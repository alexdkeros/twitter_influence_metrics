'''
Created on Feb 22, 2016

@author: ak
'''
import sys
sys.path.append('/home/ak/git/demokritos_entry_project/')


import json
import operator
import pickle
import networkx as nx
import scipy.stats as stats
from Utils.ConcatJSONDecoder import ConcatJSONDecoder
from Graphs.MentionGraph import build_mention_graph
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
    
    twitter_graph=build_mention_graph(json_data)
    
    #===========================================================================
    # computing centralities
    #===========================================================================
    
    #===========================================================================
    # degree_scores, degree_rankings=apply_centrality_algo(twitter_graph, nx.in_degree_centrality, resultsPath=resultsFolder+'degreeRankings.p')
    # 
    # betweenness_scores, betweenness_rankings=apply_centrality_algo(twitter_graph, nx.betweenness_centrality, resultsPath=resultsFolder+'betweennessRankings.p', normalized=False)
    # 
    # pagerank_scores, pagerank_rankings=apply_centrality_algo(twitter_graph, nx.pagerank, resultsPath=resultsFolder+'pagerankRankings.p')
    # 
    # follower_scores,follower_rankings=apply_centrality_algo(twitter_graph, follower_centrality, resultsPath=resultsFolder+'followerRankings.p')
    #===========================================================================
    
    euclidean_scores, euclidean_rankings=apply_centrality_algo(twitter_graph, centralities_euclidean_norm_centrality, resultsPath=resultsFolder+'euclideanNormRankings.p') 
      
    print(sorted(euclidean_scores, key=operator.itemgetter(1), reverse=True)[0:10])
    print(euclidean_rankings[0:10])
    #===========================================================================
    # computing Kendall Tau corellations
    #===========================================================================
  
#===============================================================================
#     print('Degree - Betweenness Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, betweenness_rankings ))
# 
#     print('Degree - Pagerank Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings, pagerank_rankings ))
# 
#     print('Degree - Followers Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings , follower_rankings ))
#     
#     print('Degree - Euclidean Norm Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(degree_rankings , euclidean_rankings ))
#     
#        
#        
#     print('Betweenness - Pagerank Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings , pagerank_rankings ))
#     
#     print('Betweenness - Followers Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings, follower_rankings ))
#     
#     print('Betweenness - Euclidean Norm Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(betweenness_rankings, euclidean_rankings ))
#     
#     
#     
#     print('Pagerank - Followers Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(pagerank_rankings , follower_rankings ))
#     
#     print('Pagerank - Euclidean Norm Kendall Tau corellation:')
#     print('Tau statistic: %f p-value: %f'%stats.kendalltau(pagerank_rankings , euclidean_rankings ))
#     
#===============================================================================
    
    

if __name__=='__main__':
    
    main('/home/ak/git/demokritos_entry_project/tweets.json.1',resultsFolder='/home/ak/git/demokritos_entry_project/')