# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:47:10 2023

@author: Ravit
"""

import pandas as pd


# In[]

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv').set_index('Unnamed: 0')
df.index.name = 'id'
df.columns = ['titles', 'abstract', 'link', 'source', 'abstract_bertopic_id', 'title_bertopic_id']


Levi_file = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\27Feb2023_merged_Levi_dfs_with_index.csv').set_index('id')

# In[]

df_merged = pd.concat([Levi_file, df])[Levi_file.columns]

indices = df_merged.reset_index()[['titles', 'abstract', 'bertopic_cluster_id']].drop_duplicates().index
df_merged = df_merged.reset_index().loc[indices]
df_merged = df_merged.reset_index().loc[indices].set_index('id')

# In[]
df_merged.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\7March2023_merged_Levi_dfs_with_index.csv')