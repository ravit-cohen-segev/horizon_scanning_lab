# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 19:53:42 2022

@author: Ravit
"""
# In[0]
import pandas as pd
import os
import numpy as np

folder_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic"


original_path = os.path.join(folder_path,"extracted_verbs_nouns_before_bertopic.csv")
clusters_path= os.path.join(folder_path,"verb_bertopic_clusters.csv")
labels_path = os.path.join(folder_path,"verb_bertopic_cluster_words.csv")

original_df = pd.read_csv(original_path)
clusters_df = pd.read_csv(clusters_path)
labels_df = pd.read_csv(labels_path)

# In[1]
cluster_labels = []

for i, cluster in enumerate(clusters_df['bertopic_verb_id'].to_list()):
    label = labels_df[labels_df['Topic']==cluster]['Name'].iloc[0]
    cluster_labels.append(label)


clusters_df['label'] = cluster_labels



# In[2]
#add rows without verbs to clusters_df

to_concat = original_df[original_df["spacy_verbs"].isna()]
to_concat['bertopic_verb_id'] = [np.nan]*len(to_concat)
to_concat['label'] = ["unassigend"]*len(to_concat)


# In[3]
clusters_df = pd.concat([clusters_df, to_concat])
clusters_df.to_csv(os.path.join(folder_path,"bertopic_verbs_with_labels.csv"))