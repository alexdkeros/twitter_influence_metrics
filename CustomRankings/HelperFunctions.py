'''
Created on Feb 23, 2016

@author: ak
'''
import operator
import pickle
import itertools
import scipy.stats as stats
from Utils.Visualizer import show_best_scores, show_corr_results

def apply_centrality_algo(G, rankMethod, **kwargs):
    """Applies specified ranking computation method to graph
    
    Applies ranking computation to graph, saves results and prints top 5
    
    Parameters
    ----------
    G: networkx graph
    rankMethod: bound method operating on networkx graph
        method to apply to graph
    resultPath: string, optional
        folder to save ranking results
    printRes: boolean, default True
        print results
    kwargs: arguments passed directly to method
    
    Returns
    -------
    scores: list of (node_label, score) pairs 
        sorted in descenting order
    rankings: list or rankings 
    """
    resultsPath=kwargs.pop('resultsPath', None)
    printRes=kwargs.pop('printRes',True)
    
    #DBG
    print('...%s rankings...'%rankMethod.__name__)
    
    scores_dict=rankMethod(G,**kwargs)
    scores=sorted(scores_dict.items(),key=operator.itemgetter(0))
    scores=sorted(scores,key=operator.itemgetter(1),reverse=True)
    
    if resultsPath:
        pickle.dump(scores_dict,open(resultsPath,'wb'))
    
    if printRes:
        print('Top 5 %s rankings:'%rankMethod.__name__)
        show_best_scores(scores_dict)
        
    rankings=compute_ranking(scores_dict)
    
    return scores,rankings



def compute_ranking(scores_dict):
    """Compute rankings from ordering
    
    Parameters
    ----------
    scores_dict: dictionary
        key - score pairs
    
    Returns
    -------
    rankings: list
        array of rankings (ints)
    """
    scores=sorted(scores_dict.items(),key=operator.itemgetter(0))
    scores=sorted(scores,key=operator.itemgetter(1),reverse=True)

    reference=sorted(scores_dict.keys())
    ordering=[k for k,v in scores]
    rankings=[ordering.index(i)+1 for i in reference]

    return rankings


def compute_kendalltau_corellations(meth_rankings,printRes=True):
    """Method for computing kendall tau corellations between different rankings
    
    Parameters
    ----------
    meth_rankings: dictionary
        dictionary {'method_name':ranking}
    printRes: bool, optional
        print correlations
    
    Returns
    -------
    corrs: list of tuples
        [('method_name_1', 'method_name_2', correlation, p_value), ]
    """
    corrs=[]
    for p in itertools.combinations(meth_rankings.items(), 2):
        
        z,pv=stats.kendalltau(p[0][1], p[1][1])
        
        corrs.append((p[0][0], p[1][0],z,pv))
    
    if printRes==True:
        show_corr_results(corrs)
        
    return corrs
    
def compute_overlaps(scores_m, top_percentage):
    """Compute overlaps between top x% in scores
    
    Parameters
    ----------
    scores_m: dictionary of {'method_name':[('name', score),]}, scores must have same lengths
    top_percentage : float
        percentage
    
    Returns
    -------
    ovs: list of tuples
        [('name_1', 'name_2', overlap_percent),]
    """    
    scores=scores_m
    corrs=[]
    l=min([len(s_v) for s_v in scores.values()])
    
    #sorting in descending order
    for m in scores:
        scores[m]=sorted(scores[m],key=operator.itemgetter(0))
        scores[m]=sorted(scores[m],key=operator.itemgetter(1),reverse=True)
        
        #picking top X%
        scores[m]=set([n for n, s in scores[m][0: (l*top_percentage/100)]])
        
    
    for s1, s2 in itertools.combinations(scores.items(),2):
        corrs.append((s1[0],s2[0],100*(float(len(s1[1].intersection(s2[1])))/float((l*top_percentage/100)))))
    
    
    return corrs