'''
Created on Feb 23, 2016

@author: ak
'''
import networkx as nx
from collections import Counter

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
            twitter_graph.add_node(tweet['user']['screen_name'], attr_dict={tweet['id']:tweet})
        else:
            twitter_graph.node[tweet['user']['screen_name']][tweet['id']]=tweet
            
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
    
    