'''
Created on Feb 23, 2016

@author: ak
'''
import networkx as nx
import operator
from collections import Counter
from dateutil.parser import parse

def build_mention_graph(json_data):
    """Builts directed graph based on twitter mentions
    
    Parameters
    ----------
    json_data: list of json dictionaries containing twitter data
    
    Returns
    -------
    twitter_graph: digraph 
    """
    
    #DBG
    print('...creating graph...')
    
    twitter_graph=nx.DiGraph()
    
    for tweet in json_data:
        
        #adding user as node, tweets as node attributes
        if tweet['user']['screen_name'] not in twitter_graph.nodes():
            twitter_graph.add_node(tweet['user']['screen_name'], attr_dict={'tweets':{tweet['id']:tweet}})
        elif 'tweets' not in twitter_graph.node[tweet['user']['screen_name']]:
            twitter_graph.node[tweet['user']['screen_name']]['tweets']={tweet['id']:tweet}
        else:    
            twitter_graph.node[tweet['user']['screen_name']]['tweets'][tweet['id']]=tweet
            
        #adding edges to nodes/users mentioned
        for mention in tweet['entities']['user_mentions']:
            twitter_graph.add_edge(tweet['user']['screen_name'], mention['screen_name'])
            
    
    #DBG
    print('Node count: %d'%len(twitter_graph.nodes()))
    print('Edge count: %d'%len(twitter_graph.edges()))
    
    return twitter_graph


def build_local_influence_graphs(json_data, hashtag_lower_t=None):
    """Builds directed graph based on twitter mentions, as well as local hashtag/topic based networks
    
    Parameters
    ----------
    json_data: list of json dictionaries containing twitter data
    hashtag_lower_t: int or None, optional
        process hashtags with count>hashtag_lower_t, if None, processes all hashtags
    
    Returns
    -------
    twitter_graph: digraph
    topic_subgraphs: dictionary
        dictionary of { hashtag/topic: subgraph }
    """
    
    twitter_graph=build_mention_graph(json_data)
    
    print('...locating subgraphs...')
    
    #extract hashtags
    h_list=[]
    for tweet in json_data:
        twitter_graph.node[tweet['user']['screen_name']]['hashtags']=set()
        
        if tweet['entities']['hashtags']:
            h_list.extend([h['text'] for h in tweet['entities']['hashtags']])
            
            #add hashtag attribute to node
            if 'hashtags' in twitter_graph.node[tweet['user']['screen_name']]:
                twitter_graph.node[tweet['user']['screen_name']]['hashtags']=twitter_graph.node[tweet['user']['screen_name']]['hashtags'].union(set([h['text'] for h in tweet['entities']['hashtags']]))
            else:
                twitter_graph.node[tweet['user']['screen_name']]['hashtags']=set([h['text'] for h in tweet['entities']['hashtags']])
            
    h_dict=Counter(h_list)
    
    
    #filter out low hashtag counts, if required
    if hashtag_lower_t:
        h_dict={k:h_dict[k] for k in h_dict if h_dict[k]>=hashtag_lower_t}
       
    topic_subgraphs={}
    
    #form local hashtag networks
    for k in h_dict:
        nodes=filter(lambda (n,d): k in d['hashtags'] if 'hashtags' in d else False, twitter_graph.nodes_iter(data=True))
        topic_subgraphs[k]=twitter_graph.subgraph([n for n,a in nodes])
    
    return twitter_graph, topic_subgraphs
    
    



def build_weighted_influence_graph(json_data,min_edge_weight=0.1):
    """Builds weighted directed graph based on twitter mentions, followers and hashtags
    
    weights are computed in terms of followers and hashtag percolation
    
    Parameters
    ----------
    json_data: list of json dictionaries containing twitter data
    
    Returns
    -------
    twitter_graph: digraph
    """
    
    twitter_graph=build_mention_graph(json_data)
    
    #extract hashtags
    h_list=[]
    for tweet in json_data:
        twitter_graph.node[tweet['user']['screen_name']]['hashtags']=set()
        twitter_graph.node[tweet['user']['screen_name']]['hashtag_timeline']={}
        twitter_graph.node[tweet['user']['screen_name']]['followers']=tweet['user']['followers_count']
        
        if tweet['entities']['hashtags']:
            h_list.extend([h['text'] for h in tweet['entities']['hashtags']])
            
            #add hashtag attribute to node
            if 'hashtags' in twitter_graph.node[tweet['user']['screen_name']]:
                twitter_graph.node[tweet['user']['screen_name']]['hashtags']=twitter_graph.node[tweet['user']['screen_name']]['hashtags'].union(set([h['text'] for h in tweet['entities']['hashtags']]))                
            else:
                twitter_graph.node[tweet['user']['screen_name']]['hashtags']=set([h['text'] for h in tweet['entities']['hashtags']])
            
            #add hashtag_timeline attribute to node
            if 'hashtag_timeline' in twitter_graph.node[tweet['user']['screen_name']]:
                for h in tweet['entities']['hashtags']:
                    if h['text'] in twitter_graph.node[tweet['user']['screen_name']]['hashtag_timeline']:
                        twitter_graph.node[tweet['user']['screen_name']]['hashtag_timeline'][h['text']].append(parse(tweet['created_at']))
                    else:
                        twitter_graph.node[tweet['user']['screen_name']]['hashtag_timeline'][h['text']]=[parse(tweet['created_at'])]               
            else:
                twitter_graph.node[tweet['user']['screen_name']]['hashtag_timeline']={h['text']:[parse(tweet['created_at'])]}
    
    
    h_dict=Counter(h_list)
    h_sum=sum(h_dict.values())
    #compute hashtag rarities
    h_dict_rar={h:(float(v)/float(h_sum)) for h,v in h_dict.iteritems()}
    
    #normalization of followers
    max_f=max([di['followers'] if 'followers' in di else -1 for n,di in twitter_graph.nodes_iter(data=True)])
    min_f=min([di['followers'] if 'followers' in di else max_f for n,di in twitter_graph.nodes_iter(data=True)])
    
    #add edge weights
    for i,j in twitter_graph.edges_iter():
        w_f=0.0
        w_h=0.0
        if 'followers' in twitter_graph.node[j]:
            w_f=(float(twitter_graph.node[j]['followers'])-float(min_f))/(float(max_f)-float(min_f))
            
        if ('hashtag_timeline' in twitter_graph.node[i]) and ('hashtag_timeline' in twitter_graph.node[j]):
            
            for h in set(twitter_graph.node[i]['hashtag_timeline'].keys()).intersection(twitter_graph.node[j]['hashtag_timeline'].keys()):
                if any(min(twitter_graph.node[j]['hashtag_timeline'][h])<v for v in twitter_graph.node[i]['hashtag_timeline'][h]):
                                        
                    w_h+=h_dict_rar[h]
        
        twitter_graph[i][j]['follower_weight']=w_f
        twitter_graph[i][j]['hashtag_weight']=w_h   
        twitter_graph[i][j]['weight']=min_edge_weight+w_f+w_h

    return twitter_graph
    
    