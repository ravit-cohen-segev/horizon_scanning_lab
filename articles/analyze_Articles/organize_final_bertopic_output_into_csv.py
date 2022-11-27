# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:07:57 2022

@author: Ravit
"""

import pandas as pd
import os

path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic"

path_abs_clusters = os.path.join(path,"abtracts_bertopic_clusters.csv")
path_labels = os.path.join(path, "bertopic_cluster_words.csv")

df_clusters = pd.read_csv(path_abs_clusters) 
df_labels = pd.read_csv(path_labels)

df_clusters.drop(['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True)
df_labels.drop(['Unnamed: 0'], axis=1, inplace=True)

#change cluster_id column name to topic to make it consistant

df_clusters.columns = ['link', 'abstract', 'Topic']

#sort df_clusters by topic column
df_clusters.sort_values('Topic', inplace=True)

topics = df_clusters['Topic'].to_list()

list_labels = []

for topic in topics:
    if topic == 14:
        list_labels.append('14')
        continue

    label = df_labels[df_labels['Topic']==topic]['Name'].iloc[0]
    list_labels.append(label)


df_clusters['label'] = list_labels

df_clusters = df_clusters[['Topic', 'label', 'link', 'abstract']]

#add titles and title essence from titles textrank 
sec_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results"
titles_path = os.path.join(sec_path, "titles_textrank_approved_after_final_filtering.csv")
titles_df = pd.read_csv(titles_path)

titles_df = pd.read_csv(titles_path, encoding= 'unicode_escape')

titles_list = []
clusters_links = df_clusters['link'].to_list()

for link in clusters_links:
    title = titles_df[titles_df['link']==link]['article_keywords']
    titles_list.append(title)



