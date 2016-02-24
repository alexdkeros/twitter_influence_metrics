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


def main(filename, resultsFolder=None):
    """ Analyzing influence metrics in Twitter
    
    Influence analysis via centrality methods on graph representing twitter interractions.
    
    Parameters
    ----------
    filename: string
        json file containing twitter data
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
    
    twitter_graph,hashtag_subgraphs=build_local_influence_graphs(json_data, hashtag_lower_t=5)
    
    d=hashtag_subgraphs.copy()
    d.update({'whole_graph':twitter_graph})
    
    for g_desc in d:
        
        print(g_desc+'\n\n')
        
        g=d[g_desc]
        #===========================================================================
        # computing centralities
        #===========================================================================
        
        degree_scores, degree_rankings=apply_centrality_algo(g, nx.in_degree_centrality, resultsPath=resultsFolder+g_desc+'degreeRankings.p')
         
        betweenness_scores, betweenness_rankings=apply_centrality_algo(g, nx.betweenness_centrality, resultsPath=resultsFolder+g_desc+'betweennessRankings.p', normalized=False)
         
        closeness_scores, closeness_rankings=apply_centrality_algo(g, nx.closeness_centrality,resultsPath=resultsFolder+g_desc+'closenessRankings.p')
        
        eigenvector_scores, eigenvector_rankings=apply_centrality_algo(g, nx.eigenvector_centrality, resultsPath=resultsFolder+g_desc+'eigenvectorRankings.p')
        
        current_flow_bet_scores, current_flow_bet_rankings=apply_centrality_algo(g, nx.current_flow_betweenness_centrality, resultsPath=resultsFolder+g_desc+'curFlowBetwRankings.p')
        
        pagerank_scores, pagerank_rankings=apply_centrality_algo(g, nx.pagerank, resultsPath=resultsFolder+g_desc+'pagerankRankings.p')
         
        follower_scores,follower_rankings=apply_centrality_algo(g, follower_centrality, resultsPath=resultsFolder+g_desc+'followerRankings.p')
        
        euclidean_scores, euclidean_rankings=apply_centrality_algo(g, centralities_euclidean_norm_centrality, resultsPath=resultsFolder+g_desc+'euclideanNormRankings.p') 
    
        #===========================================================================
        # computing Kendall Tau corellations
        #===========================================================================
      
        #TODO: create compact results methods
        
     #==========================================================================
     #    print('Degree - Betweenness Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, betweenness_rankings ))
     # 
     #    print('Degree - Closeness Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, closeness_rankings ))
     #    
     #    print('Degree - Eigenvector Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, eigenvector_rankings ))
     #    
     #    print('Degree - Current flow Betweenness Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, current_flow_bet_rankings ))
     #    
     #    print('Degree - Pagerank Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, pagerank_rankings ))
     # 
     #    print('Degree - Followers Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings , follower_rankings ))
     #     
     #    print('Degree - Euclidean Norm Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings , euclidean_rankings ))
     #     
     #        
     #        
     #    print('Betweenness - Pagerank Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings , pagerank_rankings ))
     #     
     #    print('Betweenness - Followers Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings, follower_rankings ))
     #     
     #    print('Betweenness - Euclidean Norm Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings, euclidean_rankings ))
     #     
     #     
     #     
     #    print('Pagerank - Followers Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(pagerank_rankings , follower_rankings ))
     #     
     #    print('Pagerank - Euclidean Norm Kendall Tau corellation:')
     #    print('Tau statistic: %f p-value: %f'%stats.kendalltau(pagerank_rankings , euclidean_rankings ))
     # 
     #==========================================================================
    
    

if __name__=='__main__':
    
    main('/home/ak/git/demokritos_entry_project/tweets.json.1',resultsFolder='/home/ak/git/demokritos_entry_project/')