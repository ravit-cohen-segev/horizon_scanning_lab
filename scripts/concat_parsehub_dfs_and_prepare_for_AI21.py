# -*- coding: utf-8 -*-
"""
Created on Thu May 18 12:56:56 2023

@author: Ravit
"""

import pandas as pd
import numpy as np
import os

# In[]
def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

# In[]

folder_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\Levi_scores_copy_from_drive\split_files_for_parsehub_text_extraction\extracted_article_texts'
df_files = os.listdir(folder_path)
dfs = []

for df_file in df_files:
    file_path = os.path.join(folder_path, df_file)
    df_ = pd.read_csv(file_path)
    if 'eit' in df_file:
        source = 'eit'
        
    if 'etn' in df_file:
        source = 'etn'
    
    if 'science_daily' in df_file:
        source = 'science_daily'
    
    df_['source'] = source
    dfs.append(df_) 

dfs = pd.concat(dfs)
dfs = dfs[dfs['links_link'].notna()]

# In[]
unique_links = list(set(dfs['links_link'].to_list()))
new_df = pd.DataFrame([], columns = ['article_link', 'article_title', 'article_text', 'source'])


for link in unique_links:
    df_ = dfs[dfs['links_link'] == link]
    df_ = df_.fillna('')
    
    #join text into one paragraph
    article_text = remove_non_ascii(" ".join(df_['links_article_text'].to_list())).replace('\n', ' ').replace('\t', '')
    article_title = list(set(df_['links_title']))[0]
    article_source = list(set(df_['source']))[0]
    
    new_df = pd.concat([new_df, pd.DataFrame([[link, article_title, article_text, article_source]], columns = ['article_link', 'article_title', 'article_text', 'source'])])
    

new_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\Levi_scores_copy_from_drive\split_files_for_parsehub_text_extraction\ai21_ready_texts\18May23_ai21_prompts.csv', index=False)

