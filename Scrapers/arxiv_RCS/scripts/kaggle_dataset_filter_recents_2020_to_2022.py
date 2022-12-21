# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 14:19:04 2022

@author: Ravit
"""

import json
import pandas as pd
import numpy as np

from collections import Counter

# In[]


with open(r'C:\Users\Ravit\Downloads\archive\arxiv-metadata-oai-snapshot.json') as f:
    data = [json.loads(line) for line in f]

# In[]    
df = pd.DataFrame(data)
# In[]
dates = df['update_date'].to_list()

# In[]
numeric_years = [int(date.split('-')[0]) for date in dates]

np.max(numeric_years)
Counter(numeric_years)

# In[]
years_recent = [2020, 2021, 2022]
rows_to_keep = [i for i, year in enumerate(numeric_years) if year in years_recent]
df = df.iloc[rows_to_keep]
# In[]
#filter out all subjects related to math and physics
f1 = open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\arxiv_RCS\scripts\docs\arxiv_categories.json')    
category_taxonomy = json.load(f1)

#create list of categories to remove
remove_categories = list(category_taxonomy['Mathematics']) + ['physics', 'cs.DM'] + list(category_taxonomy['Physics'].values())

category_list = df['categories'].to_list()

# In[]
# TODO complete filter
idx_remove = []
for i, row in df.iterrows():
    for rem in remove_categories:
        if rem in row['categories']:
            idx_remove.append(i)
    

df_filtered = df.drop(idx_remove, axis=0)
# In[]
#remove lists from cells
df_filtered.applymap(lambda x: x[0] if isinstance(x, list) else x)
# In[]
df_filtered.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\arxiv_RCS\scripts\docs\arxiv-articles-kaggle-dataset.csv')
# In[]
#divide into chunks
idx = np.arange(len(df_filtered))
idx_splits = np.array_split(idx, 500)
# In[]
for i, idx_list in enumerate(idx_splits):
    temp_df = df.iloc[idx_list]
    temp_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\arxiv_RCS\scripts\docs\arxiv-articles-kaggle-dataset-chunk' +str(i) + '.csv')
    
# In[]
