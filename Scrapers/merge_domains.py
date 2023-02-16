# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:42:01 2023

@author: Ravit
"""

import pandas as pd
import os

# In[0]
df1 = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\withouth_reddit_crunch\alon_filtered_files\3rd_iter\3rd_iter\3rd_iter_bertopic_title_cluster_id.csv')
df2 = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv')

# In[1]
#add source to df with news from techcrunch and reddit
links = df2['link'].to_list()
source_list = []

for link in links:
    if 'crunch' in link:
        source_list.append('techcrunch')
    else:
        source_list.append('other news sites')


df2['source'] = source_list
# In[2]
df1 = df1[['link', 'title', 'abstract', 'source']]
df2 = df2[['link', 'titles', 'abstract', 'source']]

df2.columns = df1.columns

# In[3]
#concat dfs
all_dfs = pd.concat([df1,df2], axis=0)
# In[4]
all_dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv')