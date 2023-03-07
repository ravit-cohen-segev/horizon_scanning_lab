# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:29:43 2023

@author: Ravit
"""
from crossref.restful import Works
from habanero import Crossref
import pandas as pd
import numpy as np
from tqdm import tqdm


# In[]
# get info about scientific articles from crossref: 
works = Works()

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv').set_index(['Unnamed: 0'])

df = df.loc[[i for i, row in df.iterrows() if row['source'] in ['arxiv', 'science_daily']]] 


# In[]

cr = Crossref()

# In[]

#pdf_url_list = [np.nan]*len(doi_list)

keep_columns = ['reference-count', 'publisher', 'short-container-title',  'DOI', 'type', 
                'is-referenced-by-count', 'title',  'container-title', 'link', 'score',  'URL', 'subject']

df_columns = ['reference-count', 'publisher',  'short-container-title',  'DOI', 'type', 
                'is-referenced-by-count', 'title',  'container-title', 'other_links', 'score',  'URL', 'subject', 'pdf_link','other_links']

# In[]


dfs_list = []
ind_list = []


#for index, row in tqdm(df.iterrows(), total=df.shape[0]):    
for index, row in df.iterrows():    
    try:
        d =  cr.works(query = row['title'])
    except:
        continue
    
    d = d['message']['items'][0]
   
    if d is None:
        continue
    if 'title' not in d.keys():
        continue
    
    if d['title'][0].lower().split() != row['title'].lower().split():
        continue
    
    ind_list.append(index)
    d_df = pd.DataFrame(np.array(['UNKNOWN']*len(df_columns)).reshape(1,14), columns=df_columns)
    
    wanted_d = {key: d[key] for key in keep_columns if key in d.keys()}

    pdf_link = 'UNKNOWN'
    
    for col in wanted_d.keys():
        if col == 'link':
            other_links = []
            for item in wanted_d['link']:
                if item[ 'content-type']=='application/pdf':
                    pdf_link = item['URL']
                else:
                    other_links.append(item['URL'])
            d_df['other_links'] = ",".join(other_links)
            d_df['pdf_link'] = pdf_link
            
        else:
                
            if isinstance(wanted_d[col], list):
                d_df[col] = "".join(wanted_d[col])
            
            elif (isinstance(wanted_d[col], int)) or isinstance(wanted_d[col], str):
                d_df[col] = wanted_d[col]
            
            elif isinstance(wanted_d[col], dict):
                d_df[col] = str(wanted_d[col])
                    
   
    dfs_list.append(d_df)
    
  
# In[] 
dfs = pd.concat(dfs_list, axis=0) 

# In[]
# set df index as df index
dfs.index = ind_list


# In[]
dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\12Feb23_crosreff_info_features.csv')
