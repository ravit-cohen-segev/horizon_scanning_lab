# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 10:23:01 2023

@author: Ravit
"""

import pandas as pd
import os

# In[]
df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\reshima_bishvil_sagi_all_semantic_relations.csv').drop(['Unnamed: 0'], axis=1)

# In[]
# create queries for life sciences terms (filtered with chatgpt)

life_sc_list =  [
    "3D Bioprinting",
    "DNA digital data storage",
    "DNA repair",
    "Enzybiotics",
    "Extracellular Vesicle-based therapies",
    "Fast protein design",
    "Neuroprosthetics",
    "Plasma Medicine",
    "Precision agriculture",
    "Synthetic milk",
    "Targeted drug delivery",
    "Urine recycling into fertilizer",
    "Voice biomarker analysis",
    "Spheroid reservoir bioartificial liver"
]

# In[]

df_ls = df[df['word'].isin(life_sc_list)]
sem_type = 'co-hyponymy'
df_ls_sem = df_ls[df_ls['semantice_type']==sem_type]
queries = []
for word in life_sc_list:
    all_sem = df_ls_sem[df_ls_sem['word']==word]['synonyms']
    if len(all_sem) != 0:
        query = '"' + word + '"'+ ' or '+ '"' + '" or "'.join(all_sem) + '"'
    else:
        query = '"' + word + '"'
    queries.append(query)
    

queries_df = pd.DataFrame(queries, columns=['query'])

queries_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\opensearch_queries\2July2023_visualization_queries.csv', index=False)