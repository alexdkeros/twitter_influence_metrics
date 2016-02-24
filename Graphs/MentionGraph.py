'''
Created on Feb 23, 2016

@author: ak
'''
import networkx as nx

def build_mention_graph(json_data):
    """Builts directed graph based on twitter mentions
    
    Parameters
    ----------
    json_data: list of json dictionaries
    
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