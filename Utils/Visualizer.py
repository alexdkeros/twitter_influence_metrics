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

def show_best_score_tweets(G, scores, top=5):
    """View tweets of top scorers
    
    Parameters
    ----------
    G: networkx graph
    scores: list of ('name', score) tuples
    top: int, optional
        top x users to print
    """
    s_s=[t for t in sorted(scores, key=operator.itemgetter(1), reverse=True)[0:top]]
    
    for n,v in s_s:
        print('\n User: %s Score: %f'%(n,v))
        print('Hashtags Used:')
        if 'hashtags' in G.node[n]:
            print(G.node[n]['hashtags'])
        print('Tweets:')
        if 'tweets' in G.node[n]:
            for t in G.node[n]['tweets'].values():
                print(t['text'].encode('utf-8'))
        
        

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