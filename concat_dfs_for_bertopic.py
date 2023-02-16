# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 11:33:02 2023

@author: Ravit
"""

import pandas as pd
import os 

# In[]
# usda files
folder = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\working_files'
files = os.listdir(folder)

dfs = pd.DataFrame([])

for file in files:
    if '.csv' in file:
        path = os.path.join(folder, file)
        df = pd.read_csv(path).set_index('Unnamed: 0')
        dfs = pd.concat([dfs, df], axis=0)
        
# drop duplicates and keep relevant columns
dfs = dfs[['doi', 'title', 'abstract', 'source']].drop_duplicates()

# In[] 
dfs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\working_files\duplicate_filtered_files.csv')



