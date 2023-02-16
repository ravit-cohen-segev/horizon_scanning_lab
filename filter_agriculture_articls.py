# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:21:31 2023

@author: Ravit
"""

import pandas as pd
import json

# In[]
crunch_reddit = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\after_filtering_articles_reddit_and_crunch\filtered_articles.csv')
tech_networks = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\technology_networks_RCS\scrapped_docs\all_articles_after_fix_parsing.csv')

other_domains = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\arxiv_etn_eit_scidaily_sample.csv') 


# In[]
# add source feature to crunch and reddit
source_list = []
for i, row in crunch_reddit.iterrows():
    if 'crunch' in row['link']:
        source_list.append('techcrunch')
    elif 'reddit' in row['link']:
        source_list.append('reddit')
    else:
        source_list.append('other sources')

# In[]
title_list = crunch_reddit['title'].to_list() + other_domains['title'].to_list() + tech_networks['titles'].to_list()
title_list = [title.lower() for title in title_list]

source_list =source_list + other_domains['source'].to_list() + tech_networks['source'].to_list()

df = pd.DataFrame([])

df['title'] = title_list
df['source'] = source_list
# In[]
f = open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\dict\agriculture_terms.json')
ag_dict = json.loads(f.read())

keep_idx = []

for i, row in df.iterrows():
    for term in ag_dict['ag_terms']:
        if term in row['title']:
            keep_idx.append(i)
            break
        
df = df.iloc[keep_idx]
  
df.drop_duplicates(inplace=True)
# In[]
df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\docs\aggriculure_articles.csv')
            
            