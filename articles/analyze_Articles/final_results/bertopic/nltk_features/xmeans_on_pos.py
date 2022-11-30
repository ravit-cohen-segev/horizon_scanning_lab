# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 15:28:07 2022

@author: Ravit
"""

# In[0]
import pandas as pd 
import numpy as np

from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

# In[1]
np.random.seed(42)

pos_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_ordinal_vector_space.csv")
text_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")

pos_df.drop(['Unnamed: 0'], axis=1, inplace=True)

# In[9]
onehot_matrix = np.load(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_with_pos_mat.npy")
# In[10]
#remove features with low variance
onehot_df = pd.DataFrame(onehot_matrix)
variance = onehot_df.var()

variable = [ ]

for i in range(0,len(variance)):
    if variance[i]>=0.12: #setting the threshold as 1%
        variable.append(i)

onehot_matrix = onehot_df[variable].to_numpy()
# In[]
#add features related to verbs, number of verbs, number of present tense verbs, number of vbg, number of nouns
noun_index = [11, 16, 38, 40]
verb_index = [2, 8, 10, 28, 36]
verb_vbg = 6
verb_present = 8

title_total_words = []
all_noun_count = []
all_verb_count = []
all_verb_present = []
all_vbg = []

for i, row in pos_df.iterrows():
    row_value_counts = row.value_counts() 
    word_idx = row_value_counts.index
    if -1 in word_idx:
        word_idx = word_idx.drop(-1)
    word_num = np.sum([row_value_counts[j] for j in word_idx])
    title_total_words.append(word_num)
    
    
    noun_counts = np.sum([row_value_counts[j] for j in noun_index if j in row_value_counts])
    all_noun_count.append(noun_counts/word_num)
    verb_counts =  np.sum([row_value_counts[j] for j in verb_index if j in row_value_counts]) 
    all_verb_count.append(verb_counts/word_num)
    if verb_present in row_value_counts.index:
        count_verb_present = row_value_counts[verb_present]
        all_verb_present.append(count_verb_present/word_num)
    else:
        all_verb_present.append(0)
    if verb_vbg in row_value_counts.index:
        count_vbg = row_value_counts[verb_vbg]
        all_vbg.append(count_vbg/word_num)
    else:
        all_vbg.append(0)
    




# In[11]
# Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
# start analysis.
amount_initial_centers = 3
initial_centers = kmeans_plusplus_initializer(onehot_matrix, amount_initial_centers).initialize()

# Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
# number of clusters that can be allocated is 20.
xmeans_instance = xmeans(onehot_matrix, initial_centers, 20)
xmeans_instance.process()
 
# Extract clustering results: clusters and their centers
clusters = xmeans_instance.get_clusters()
centers = xmeans_instance.get_centers()
 
# Print total sum of metric errors
print("Total WCE:", xmeans_instance.get_total_wce())
# In[11]

out_pos_df = text_df[['link', 'titles', 'abstract']]
cluster_list = [np.nan]*len(out_pos_df)

for c_id in range(len(clusters)):
    for i in clusters[c_id]:
        cluster_list[i] = c_id
# In[]

out_pos_df['xmeans_labels'] = cluster_list
out_pos_df = out_pos_df.sort_values(by='xmeans_labels')

text_df['xmeans_labels'] = cluster_list
text_df = text_df.sort_values(by='xmeans_labels')
# In[]
text_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\xmeans_clusters_first_attempt.csv")
