# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 09:41:15 2022

@author: Ravit
"""

import pandas as pd
import os
import re

# In[]
# join all files into one table
path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\EIT_RCS\scrapped_articles\smaller_docs"
os.chdir(path)

files = os.listdir()

df = pd.DataFrame([])

for file in files:
    temp_df = pd.read_csv(os.path.join(path, file))
    df = pd.concat([df, temp_df])


# In[]
# find two words that are joined, and separate with a dot. A start of a new sentence

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)
        
# In[]
df_copy = df.copy()

for i, row in df_copy.iterrows():
    df_copy['titles'].iloc[i] = remove_non_ascii(row['titles']) 
    df_copy['summary'].iloc[i] = remove_non_ascii(row['summary'])
    
# In[]
    

df_copy.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\EIT_RCS\scrapped_articles\all_eit_news.csv")
