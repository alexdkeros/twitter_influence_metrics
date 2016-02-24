'''
Created on Feb 22, 2016

@author: ak
'''

import json
import operator
import pickle
import time
import networkx as nx
import matplotlib.pyplot as plt
import scipy.stats as stats
from Utils.ConcatJSONDecoder import ConcatJSONDecoder
from Graphs.MentionGraph import *
from CustomRankings.UserAttributeRankings import *
from CustomRankings.HelperFunctions import *
from Utils.Visualizer import show_best_score_tweets


def main_simple(filename, centralities_methods, resultsFolder=None,save=True):
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
    save: boolean, optional
        save results to pickle files
        
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
     
    d={'whole_graph':twitter_graph})
     
    #graph specific results {'graph':{res_dict}}
    g_results={}
     
    for g_desc in d:
         
        print('\n\n...Processing %s graph...\n\n:'%g_desc)
         
        #method specific results for certain graph {'method_name':(scores,rankings)}
        res_dict={'scores':{}, 'kendallTau':[], 'overlaps':[]}
         
        g=d[g_desc]
        #===========================================================================
        # computing centralities
        #===========================================================================
         
        for g_m,kwargs in centralities_methods:
             
            #{'method_name':(scores, rankings)} dictionary
            res_dict['scores'][g_m.__name__]=apply_centrality_algo(g, g_m, resultsPath=resultsFolder+g_desc+g_m.__name__+'scoreDicts.p' if save else None, **kwargs)
             
            show_best_score_tweets(d[g_desc],res_dict['scores'][g_m.__name__][0])
        
        #===========================================================================
        # computing Kendall Tau corellations
        #===========================================================================        
         
        res_dict['kendallTau']=compute_kendalltau_corellations({k:res_dict['scores'][k][1] for k in res_dict['scores']}, printRes=True)
     
        res_dict['overlaps']=compute_overlaps({n:s[0] for n,s in res_dict['scores'].items()}, top_percentage=10)

        g_results={g_desc:res_dict}
        
    #save all
    if save:
        pickle.dump(g_results,open(resultsFolder+'overalls.p','wb'))
        pickle.dump(d, open(resultsFolder+'graphs.p', 'wb'))
     
     
     
     
def main_local_networks(filename, centralities_methods, resultsFolder=None,save=True):
    """ Analyzing influence metrics in Twitter
    
    Influence analysis via centrality methods on graph representing twitter interractions as well as local networks.
    
    Parameters
    ----------
    filename: string
        json file containing twitter data
    centralities_methods: list
        list of centrality methods to apply
    resultsFolder: string, optional
        folder path to save rankings
    save: boolean, optional
        save results to pickle files
        
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
    
    twitter_graph,hashtag_subgraphs=build_local_influence_graphs(json_data, hashtag_lower_t=400)
     
    d=hashtag_subgraphs.copy()
    d.update({'whole_graph':twitter_graph})
     
    #graph specific results {'graph':{res_dict}}
    g_results={}
     
    for g_desc in d:
         
        print('\n\n...Processing %s graph...\n\n:'%g_desc)
         
        #method specific results for certain graph {'method_name':(scores,rankings)}
        res_dict={'scores':{}, 'kendallTau':[], 'overlaps':[]}
         
        g=d[g_desc]
        #===========================================================================
        # computing centralities
        #===========================================================================
         
        for g_m,kwargs in centralities_methods:
             
            #{'method_name':(scores, rankings)} dictionary
            res_dict['scores'][g_m.__name__]=apply_centrality_algo(g, g_m, resultsPath=resultsFolder+g_desc+g_m.__name__+'scoreDicts.p' if save else None, **kwargs)
             
            show_best_score_tweets(d[g_desc],res_dict['scores'][g_m.__name__][0])
        
        #===========================================================================
        # computing Kendall Tau corellations
        #===========================================================================        
         
        res_dict['kendallTau']=compute_kendalltau_corellations({k:res_dict['scores'][k][1] for k in res_dict['scores']}, printRes=True)
     
        res_dict['overlaps']=compute_overlaps({n:s[0] for n,s in res_dict['scores'].items()}, top_percentage=10)

        g_results={g_desc:res_dict}
        
    #save all
    if save:
        pickle.dump(g_results,open(resultsFolder+'overalls.p','wb'))
        pickle.dump(d, open(resultsFolder+'graphs.p', 'wb'))
     
     
     
     
     
def main_weighted(filename, centralities_methods, resultsFolder=None,save=True):
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
    save: boolean, optional
        save results to pickle files
        
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
    
    twitter_graph=build_weighted_influence_graph(json_data)
     
    d={'weighted_graph':twitter_graph})
     
    #graph specific results {'graph':{res_dict}}
    g_results={}
     
    for g_desc in d:
         
        print('\n\n...Processing %s graph...\n\n:'%g_desc)
         
        #method specific results for certain graph {'method_name':(scores,rankings)}
        res_dict={'scores':{}, 'kendallTau':[], 'overlaps':[]}
         
        g=d[g_desc]
        #===========================================================================
        # computing centralities
        #===========================================================================
         
        for g_m,kwargs in centralities_methods:
             
            #{'method_name':(scores, rankings)} dictionary
            res_dict['scores'][g_m.__name__]=apply_centrality_algo(g, g_m, resultsPath=resultsFolder+g_desc+g_m.__name__+'scoreDicts.p' if save else None, **kwargs)
             
            show_best_score_tweets(d[g_desc],res_dict['scores'][g_m.__name__][0])
        
        #===========================================================================
        # computing Kendall Tau corellations
        #===========================================================================        
         
        res_dict['kendallTau']=compute_kendalltau_corellations({k:res_dict['scores'][k][1] for k in res_dict['scores']}, printRes=True)
     
        res_dict['overlaps']=compute_overlaps({n:s[0] for n,s in res_dict['scores'].items()}, top_percentage=10)

        g_results={g_desc:res_dict}
        
    #save all
    if save:
        pickle.dump(g_results,open(resultsFolder+'overalls.p','wb'))
        pickle.dump(d, open(resultsFolder+'graphs.p', 'wb'))
     