# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:43:59 2023

@author: Ravit
"""

import pandas as pd
from fastai.text.all import *

# In[]
# Define paths to files
org_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv'
path2 = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\model_input\2Feb23all_features.csv'

# Load text files as dataframes
df_main = pd.read_csv(org_path)
df2 = pd.read_csv(path2)


# In[]
def check_if_unnamed_in_cols(df):
    for col in df.columns:
        assert('Unnamed' not in col)
            
        
def test_indices_eq(df_main, df):
    # Compare indices and check for matches
    match = (df_main.index == df.index).all()

    try:    
        assert(match)
        print('Indices match')
    except:
        print('Indices do not match')

# In[]
check_if_unnamed_in_cols(df2)