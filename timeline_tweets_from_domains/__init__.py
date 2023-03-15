# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:51:19 2023

@author: Ravit
"""

import pandas as pd

import os 

os.chdir(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\lib\timeline_tweets_from_domains')
from myfunctions import *


# In[]
NYT_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\NYT_RCS\docs\headlines\csv_converted_files'
TN_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\technology_networks_scrapped'

tech_syns = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\9March23_tech_synonyms_and_names - Sheet1.csv').set_index('Tech_Name')
# In[]








# In[]

tech_dict = tech_names.T.to_dict()

for key in tech_dict.keys():
    tech_values = tech_dict[key].values()
    tech_values = [val for val in tech_values if type(val) is str]
    tech_dict[key] = tech_values
    
# In[]
df_counts_NYT = create_tech_list_timeseries_news_titles_NYT(tech_dict, NYT_path)