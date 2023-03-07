# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:12:55 2023

@author: Ravit
"""

import pandas as pd

df_to_add_index = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\New_EMT_26_02_23.xlsx')
df_with_index = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv').set_index('Unnamed: 0')
df_with_index.index.name = 'id'

# In[]

index_list = []

for i, row in df_to_add_index.iterrows():
    index_list.append(df_with_index[df_with_index['title'] == row['titles']].index.to_list())

df_to_add_index['id'] = index_list
df_to_add_index.set_index('id', inplace=True)
      

df_to_add_index.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\New_EMT_26_02_23_with_index.csv')
    

# In[]
#merge with previous tech df Levi
Levi_prev_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\xmeans_clusters_fourth_attempt_levi_scores_with_index.csv').set_index('id')
cols = [col for col in Levi_prev_df.columns if 'Unnamed' not in col]

Levi_prev_df = Levi_prev_df[cols]


# In[]

same_cols = [col for col in df_to_add_index if col in Levi_prev_df.columns]
df_to_add_index_ = df_to_add_index[same_cols]

# diff cols 1 are the original columns
diff_cols_1 = [col for col in Levi_prev_df.columns if col not in df_to_add_index.columns]
diff_cols_2 = [col for col in df_to_add_index.columns if col not in Levi_prev_df.columns]


# In[]
#levi_cols = same_cols + diff_cols_1
#Levi_prev_df_ = Levi_prev_df[levi_cols]

# In[]
df_add2 = df_to_add_index[['New_Tech_code', 'Levi_Related_Class (1,2,3,0)  by defined categories in Sheet 1', 'Levi_Stage_assessment']]
df_add2.columns = ['new_Tech_code (1-new application. 2- new subtech. 3- completely new tech)', 'Levi_Related_Class (1,2,3,0)  by defined categories in Sheet 1 ', 'stage_assesment']

df_to_add_index_ = pd.concat([df_to_add_index_, df_add2], axis=1)

#print cols that are missing in the new add df 
missing_cols = list(set(Levi_prev_df.columns) - set(df_to_add_index_.columns))

df_to_add_index_[missing_cols] = None


df_to_add_index_ = df_to_add_index_[Levi_prev_df.columns]







# In[]
merged_df = pd.concat([Levi_prev_df, df_to_add_index_], axis=0)
merged_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\27Feb2023_merged_Levi_dfs_with_index.csv')


