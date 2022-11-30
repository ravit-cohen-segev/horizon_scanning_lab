# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:41:07 2022

@author: Ravit
"""

import pandas as pd
import numpy as np
from nltk.data import load
import os

path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features"
pos_path = os.path.join(path, "POS_ordinal_vector_space.csv")
xmeans_path = os.path.join(path, "xmeans_clusters_first_attempt.csv")

pos_df = pd.read_csv(pos_path)
pos_df.drop(['Unnamed: 0'], axis=1, inplace=True)

tagdict = load('help/tagsets/upenn_tagset.pickle')
feature_list =  list(tagdict.keys()) + [ 'None']

noun_index = [11, 16, 38, 40]
verb_index = [2, 8, 10, 28, 36]
verb_vbg = 6
verb_present = 8

xmeans_df = pd.read_csv(xmeans_path)
xmeans_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
# In[]
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
    
# In[]
df_stats = xmeans_df['xmeans_labels'].to_frame()
df_stats['noun_total'] = all_noun_count
df_stats['verb__total'] = all_verb_count
df_stats['verb_present'] = all_verb_present
df_stats['verb_vbg'] = all_vbg

# In[]
groups = df_stats.groupby('xmeans_labels')
group_stats = groups.sum()
# In[]
group_stats.to_csv(os.path.join(path, "xmeans_statistics.csv"))   