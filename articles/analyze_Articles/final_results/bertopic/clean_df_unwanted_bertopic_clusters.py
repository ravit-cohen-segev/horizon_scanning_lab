# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 21:49:03 2022

@author: Ravit
"""

import pandas as pd

path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\jaccard_titles_after_bertopic_clusters.csv"
labels_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\jaccard_filtered_bertopic_cluster_words.csv"

df = pd.read_csv(path)
df_labels = pd.read_csv(labels_path)

df.drop(['title_sim_tag', 'abs_sim_tag'], axis=1, inplace=True)


clusters_id_to_remove = [-1,0,7,8]
df['cluster_Name'] = [df_labels[df_labels['Topic']==val]['Name'].iloc[0] for val in df['bertopic_cluster_id'].to_list()]

df = df.iloc[[i for i, val in enumerate(df['bertopic_cluster_id']) if val not in clusters_id_to_remove]]

df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True)
df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering.csv")

