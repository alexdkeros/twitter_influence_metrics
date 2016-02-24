'''
Created on Feb 24, 2016

@author: ak
'''
import operator

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
    
    for i in range(min(top,len(scores))):
        print('Name: %s Score: %f'%(scores[i][0],scores[i][1]))


def show_corr_results(corrs):
    """View correlation between methods
    
    Parameters
    ----------
    corrs: list of tuples
        containing [('name_1','name_2', corr_value, p_value),]
    """
    for c in corrs:
        print('\n%s - %s Kendall Tau corellation:'%(c[0],c[1]))
        print('Tau statistic: %f p-value: %f'%(c[2],c[3]))