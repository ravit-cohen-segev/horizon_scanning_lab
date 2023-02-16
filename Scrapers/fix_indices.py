# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:24:20 2023

@author: Ravit
"""

import pandas as pd


# In[]

df_to_fix = pd.read_excel(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\alon_files_after_clusteirng\New_Domains_Eval_Tech_Levi_Marked.xlsx')

# In[]
df_correct_index = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv')

# In[]
index_list = []


for i, row in df_to_fix.iterrows():
    title = row['titles']
    index_list.append(df_correct_index[df_correct_index['title']==title]['Unnamed: 0'].iloc[0])
    
    
# In[]
df_to_fix.index = index_list

df_to_fix.drop(['att1'], axis=1, inplace=True)


# In[]
df_to_fix.index.rename('id', inplace=True)

df_to_fix.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\alon_files_after_clusteirng\New_Domains_Eval_Tech_Levi_Marked_with_index.csv')