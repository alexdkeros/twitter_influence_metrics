'''
Created on Feb 22, 2016

@author: ak
'''
import math
import networkx as nx

def follower_centrality(G):
    """Create user ranking based on user followers
    
    Parameters
    ----------
    G: networkX graph
        graph with 'screen_name' as node labels, tweet dictionary {<tweet_id>:tweet, } as attribute dictionary
    
    Returns
    -------
    nodes: dictionary
        Dictionary of nodes with follower count as value
        If no data for user, set value==-1
    """
    nodes={}
    for n in G.nodes():
        
        if G.node[n]:
            if ('tweets' in G.node[n]) and G.node[n]['tweets']:
                nodes[n]=G.node[n]['tweets'].values()[0]['user']['followers_count']
        else:
            nodes[n]=-1
    
    return nodes


def centralities_euclidean_norm_centrality(G, weight=None, distance=None):
    """Implementation of Euclidean norm of centralities as centrality measure
    
    Centrality measure is the Euclidean norm of the normalized Degree, Closeness and Betweenness centralities,
    as described in [1] .
    
    Parameters
    ----------
    G: networkx graph
        graph representing social network
    weight: string or None, optional
        weight edge attribute for betweenness centrality
    distance: string or Node, optional
        distance edge attribute for closeness centrality
        
    Returns
    -------
    nodes: dictionary
        Dictionary of nodes with euclidean norm score as value
    
    
    References
    ----------
    ..[1] Na Li; Gillet, D., "Identifying influential scholars in academic social media platforms,"
        in Advances in Social Networks Analysis and Mining (ASONAM), 
        2013 IEEE/ACM International Conference on , vol., no., pp.608-614, 25-28 Aug. 2013
    """
    
    #normalizing function
    #Parameters : x - value, di - dictionary
    #Returns : normalized value (x-min(di)) / (max(di)-min(di))
    normalizing=lambda x,di: ((x-min(di.values()))/(max(di.values())-min(di.values()))) if (max(di.values())-min(di.values()))!=0 else 0

    #degree centrality
    deg_dict=nx.in_degree_centrality(G)
    deg_dict={k:normalizing(v,deg_dict) for k,v in deg_dict.items()}
    
    #closeness centrality
    clo_dict=nx.closeness_centrality(G, distance=distance)
    clo_dict={k:normalizing(v,clo_dict) for k,v in clo_dict.items()}
    
    #betweenness centrality
    betw_dict=nx.betweenness_centrality(G, weight=weight)
    betw_dict={k:normalizing(v,betw_dict) for k,v in betw_dict.items()}
    
    #euclidean norm
    nodes={k: math.sqrt( (deg_dict[k])**2 + (clo_dict[k])**2 + (betw_dict[k])**2 ) for k in G.nodes()}
    
    return nodes
        
    