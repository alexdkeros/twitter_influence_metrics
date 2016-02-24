'''
Created on Feb 23, 2016

@author: ak
'''
import operator
import pickle

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



def show_best_scores(scores_dict,top=5):
    """View top scores
    
    Parameters
    ----------
    scores_dict: dictionary
        key - score enties
    top: int, optional
        top scores to print
    """
    scores=sorted(scores_dict.items(),key=operator.itemgetter(0))
    scores=sorted(scores,key=operator.itemgetter(1),reverse=True)
    
    for i in range(top):
        print('Name: %s Score: %f'%(scores[i][0],scores[i][1]))
        
