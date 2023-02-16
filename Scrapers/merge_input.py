# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:59:39 2023

@author: Ravit
"""

import pandas as pd
import numpy as np
import re
import os

path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features'


# In[]

text_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv').set_index(['Unnamed: 0'])

# dfs with bertopic

bertopic_no_reddit_crunch_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\withouth_reddit_crunch\alon_filtered_files\3rd_iter\3rd_iter\3rd_iter_bertopic_title_cluster_id.csv')
bertopic_reddit_crunch_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv').set_index(['Unnamed: 0'])
# In[]:
#create new index for df
abstract_index = []

for index, row in text_df.iterrows():
    abstract=row["abstract"]
    abstract_index.extend([row['source']+str(index)])


text_df.index = abstract_index
# In[]
text_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv')

# In[]
#create new index for df
abstract_index = []

for index, row in bertopic_no_reddit_crunch_df.iterrows():
    abstract=row["abstract"]
    abstract_index.extend([row['source']+str(index)])


bertopic_no_reddit_crunch_df.index = abstract_index  

# In[]
# This table is missing source columne so let's create it

source_list = []
index_list = []

for i, row in bertopic_reddit_crunch_df.iterrows():
    if 'crunch' in row['link']:
        val = 'techcrunch'
        
    else:
        val = 'other news sites'
   
    source_list.append(val)
    index_list.append(val+str(i))

bertopic_reddit_crunch_df['source'] = source_list
bertopic_reddit_crunch_df.index = index_list

# In[]
bertopic_reddit_crunch_df.columns = ['link', 'title', 'abstract', 'bertopic_cluster_id', 'title_bertopic_id', 'source']
bertopic_reddit_crunch_df['abstract_bertopic_id'] = [np.nan]*len(bertopic_reddit_crunch_df)
# In[]
bertopic_reddit_crunch_df.drop(['bertopic_cluster_id'], axis=1, inplace=True)
bertopic_no_reddit_crunch_df.drop(['Unnamed: 0'], axis=1, inplace=True)

# In[]
bertopic_reddit_crunch_df = bertopic_reddit_crunch_df[bertopic_no_reddit_crunch_df.columns]

# In[]
# save a df that contains all indices and bertopic clusters into one df
bertopic_all_dfs = pd.concat([bertopic_no_reddit_crunch_df, bertopic_reddit_crunch_df], axis=0)

bertopic_all_dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv')

# In[]

file_names = ['2Feb23_all_domains_with_reddit_sentence_features.csv', '2Feb23count_ent_dep_abstracts.csv']

df_list = []

for file in file_names:
    full_path = os.path.join(path, file)
    df = pd.read_csv(full_path).set_index(['Unnamed: 0'])
    df_list.append(df)
    
dfs = df_list[0].join(df_list[1])
dfs.index = text_df.index

dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\model_input\2Feb23all_features.csv')


# In[]

# add tags to Levi's file to avoid confusion
Levi_file = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\alon_files_after_clusteirng\xmeans_clusters_fourth_attempt levi scores.csv', encoding="ISO-8859-1")

# In[]
title_index = []
for i, row in Levi_file.iterrows():
    title = row['titles']
    index = text_df.loc[text_df['title']==title].index[0]
    title_index.append(index)
    
Levi_file['index'] = title_index
Levi_file.set_index('index', inplace=True)
    
Levi_file.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\alon_files_after_clusteirng\xmeans_clusters_fourth_attempt_levi_scores_with_index.csv')


# In[]
'''
abstract_bertopic_ids = bertopic_df['abstract_bertopic_id'].to_list() 
title_bertopic_ids = bertopic_df['title_bertopic_id'].to_list() 

list_abs_ids = []
list_title_ids = []

for abs_bert, title_bert in list(zip(abstract_bertopic_ids, title_bertopic_ids)):
    if '-1' in abs_bert:
        list_abs_ids.append('-1')
    else:
        list_abs_ids.append(re.sub("[^\d\.]", "", abs_bert))
        
    if '-1' in title_bert:
        list_title_ids.append('-1')
    else:
        list_title_ids.append(re.sub("[^\d\.]", "", title_bert))'''
    
    
        




# In[]

dfs['abstract_bertopic_id'] = list_abs_ids


dfs['title_bertopic_id'] = list_title_ids


# In[]
#save dfs
dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\model_input\31Jan2023_sentence_features.csv')