'''
Created on Feb 22, 2016

@author: ak
'''
import sys
from networkx.algorithms.centrality.eigenvector import eigenvector_centrality
sys.path.append('/home/ak/git/demokritos_entry_project/')


import json
import operator
import pickle
import networkx as nx
import scipy.stats as stats
from Utils.ConcatJSONDecoder import ConcatJSONDecoder
from Graphs.MentionGraph import *
from CustomRankings.UserAttributeRankings import *
from CustomRankings.HelperFunctions import *


def main(filename, centralities_methods, resultsFolder=None):
    """ Analyzing influence metrics in Twitter
    
    Influence analysis via centrality methods on graph representing twitter interractions.
    
    Parameters
    ----------
    filename: string
        json file containing twitter data
    centralities_methods: list
        list of centrality methods to apply
    resultsFolder: string, optional
        folder path to save rankings
        
    """
    
    #===========================================================================
    # reading json file
    #===========================================================================
    
    #DBG
    print('...reading json...')
    
    with open(filename) as json_file:
        json_data=json.load(json_file, cls=ConcatJSONDecoder)
    
    
    #===========================================================================
    # building graph
    #===========================================================================
    
    twitter_graph,hashtag_subgraphs=build_local_influence_graphs(json_data, hashtag_lower_t=30)
    
    d=hashtag_subgraphs.copy()
    d.update({'whole_graph':twitter_graph})
    
    #graph specific results {'graph':{res_dict}}
    g_results={}
    
    for g_desc in d:
        
        print('\n\n...Processing %s graph...\n\n:'%g_desc)
        
        #method specific results for certain graph {'method_name':(scores,rankings)}
        res_dict={}
        
        g=d[g_desc]
        #===========================================================================
        # computing centralities
        #===========================================================================
        
        for g_m,kwargs in centralities_methods:
            
            #{'method_name':(scores, rankings)} dictionary
            res_dict[g_m.__name__]=apply_centrality_algo(g, g_m, resultsPath=resultsFolder+g_desc+g_m.__name__+'Rankings.p', **kwargs)
            
        
        g_results={g_desc:res_dict}
        #===========================================================================
        # computing Kendall Tau corellations
        #===========================================================================        
        
        compute_kendalltau_corellations({k:res_dict[k][1] for k in res_dict}, printRes=True)
    
        compute_overlaps({n:s[0] for n,s in res_dict.items()}, top_percentage=10)

if __name__=='__main__':
    dataset_path='/home/ak/git/demokritos_entry_project/tweets.json.1'
    resultsFolder='/home/ak/git/demokritos_entry_project/'
    centralities_methods=[(nx.in_degree_centrality,{}),
                          #(nx.betweenness_centrality,{'normalized':False}),
                          #(nx.pagerank,),
                          #(eigenvector_centrality,),
                          (follower_centrality,{})]
                          #(centralities_euclidean_norm_centrality,)]
    main(dataset_path,centralities_methods,resultsFolder=resultsFolder)