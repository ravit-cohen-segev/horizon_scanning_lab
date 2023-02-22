# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:43:59 2023

@author: Ravit
"""

import pandas as pd
from fastai.text.all import *



# In[]
def check_if_unnamed_in_cols(df):
    for col in df.columns:
        assert('Unnamed' not in col)
    assert('Unnamed' in df.index.name is False)
            
        
def check_if_indices_match_main_df(df_main, dfs):
    # Compare indices and check for matches   
    for df in dfs:
        match = (df_main.index == df.index).all()
        assert(match)

        

def check_if_nan_in_df(df):
    assert(df.isna().any().any() is False)

def check_all_unindented(df, col):
    text_col = df[col].to_list()
    for text in text_col:
        assert(text == " ".join(text.split()))
                   
        
def check_if_row_id_start_from_one(df):
    index_list = df.index
    first_index = "".join([i for i in index_list[0] if i.isdigit()])
    assert(first_index==1)


    
    
# In[]
if __name__=="__main__":
    # Define paths to files
    org_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\bertopic\9Feb23_all_domains_with_bertopic_ids.csv'
    path2 = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\features\model_input\2Feb23all_features.csv'
    
    # Load text files as dataframes
    df_main = pd.read_csv(org_path)
    df2 = pd.read_csv(path2)
    
    check_all_unindented(df_main, 'title')           
    
    
    df2 = df2.set_index('Unnamed: 0')
    df_main = df_main.set_index('Unnamed: 0')
    
    test_indices_eq(df2, df_main)