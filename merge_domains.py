# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:42:01 2023

@author: Ravit
"""

import pandas as pd
import os

# In[0]
df_usda_solutions = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\usda_agriculture_solutions.csv')

df_usda_problems = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\usda_agriculture_problems.csv')
df_crunch = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\techcrunch_RCS\scrapped_titles\techcrunch_scrapped_ag_titles.csv')


# In[2]
df_usda_solutions = df_usda_solutions[['id', 'title', 'abstract', 'source']]
df_usda_problems = df_usda_problems[['id', 'title', 'abstract', 'source']]

df_crunch = df_crunch[['link', 'title', 'source']]
df_crunch.columns = ['id', 'title', 'source']


# In[3]
#concat dfs
all_solutions = pd.concat([df_usda_solutions,df_crunch], axis=0)
all_problems = pd.concat([df_usda_problems,df_crunch], axis=0)
# In[4]
all_dfs.to_csv(r'')