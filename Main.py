'''

*************************TWITTER ANALYSER******************************

to run update following paths

set save=False to not save results

@author: ak
'''
import sys
sys.path.append('/home/ak/git/demokritos_entry_project/')


import networkx as nx
from TwitterAnalyser import main
from CustomRankings.UserAttributeRankings import *

if __name__=='__main__':
    
    dataset_path='/home/ak/git/demokritos_entry_project/tweets.json.1'
    resultsFolder='/home/ak/git/demokritos_entry_project/'
    centralities_methods=[(nx.in_degree_centrality,{}),
                          (nx.betweenness_centrality,{'normalized':False}),
                          (nx.pagerank,{}),
                          (nx.eigenvector_centrality,{}),
                          (follower_centrality,{}),
                          (centralities_euclidean_norm_centrality,{})]
    main(dataset_path,centralities_methods,resultsFolder=resultsFolder, save=True)