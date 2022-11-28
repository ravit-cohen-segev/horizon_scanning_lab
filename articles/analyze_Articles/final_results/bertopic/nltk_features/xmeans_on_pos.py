# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 15:28:07 2022

@author: Ravit
"""

# In[0]
import pandas as pd 
import numpy as np
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
# In[1]
df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\extracted_POS.csv")
text_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")

df_features = df.drop(['Unnamed: 0', 'Names'], axis=1) 
#drop features with single value

#for col in df_features.columns:
 #   if len(df_features[col].unique()) == 1:
  #      df_features.drop(col,inplace=True,axis=1)
# In[1]

# Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
# start analysis.
amount_initial_centers = 5
initial_centers = kmeans_plusplus_initializer(df_features, amount_initial_centers).initialize()

# In[3]
 
# Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
# number of clusters that can be allocated is 20.
xmeans_instance = xmeans(df_features, initial_centers, 20)
xmeans_instance.process()
 
# Extract clustering results: clusters and their centers
clusters = xmeans_instance.get_clusters()
centers = xmeans_instance.get_centers()
 
# Print total sum of metric errors
print("Total WCE:", xmeans_instance.get_total_wce())
 
# In[4]
out_df = text_df[['link', 'titles', 'abstract']]
cluster_list = [np.nan]*len(out_df)

for c_id in range(len(clusters)):
    for i in clusters[c_id]:
        cluster_list[i] = c_id


out_df['xmeans_labels'] = cluster_list

out_df.sort_values(by='xmeans_labels', inplace=True)

out_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\xmeans_results.csv")