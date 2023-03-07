# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:40:16 2023

@author: Ravit
"""

from googlesearch import search
import pandas as pd

# In[]

df= pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\7March2023_merged_Levi_dfs_with_index.csv')

tech_names = df['Tech_Name'].dropna()

# In[]

syns_links = {}


for i, tech_name in enumerate(tech_names):
    print(i)
    syn = []

    try:
        syn = list(search(tech_name, num_results=5))
    
    except TimeoutError:
       continue

    
    syns_links[tech_name] = syn

     

