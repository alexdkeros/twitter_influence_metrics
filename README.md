Twitter infuence metrics
========================

@NCSR Demokritos

‘REVEAL-REVEALing hidden concepts in Social Media’ (Ε-11834) program, research and development in knowledge extraction from graphs representing
Social Networks.

Exploring the concept of influence in a social media platform (Twitter). Investigation of simple metrics of influence, comparisons in terms of correlation.
Presentation slides can be found [here](https://github.com/alexdkeros/twitter_influence_metrics/blob/master/presentation/Twitter_Influence_Analysis.pdf).

Instructions/How-to run  
------------------------
1. edit `Main.py` file, replace paths and parameters as desired.  
   Params:
   `save`         : saves results into pickle files  
   `resultsFolder`: folder path to save results, if desired  
   `dataset_path` : location of dataset  
   `type`           : 
      * `simple` : simple graph and centrality measures  
      * `local_networks`: graph and local network subgraphs, running centralities on overall graph as well as local networks  
      * `weighted`: creating weighted graph and running weighted centralities

2. `python Main.py` to run
