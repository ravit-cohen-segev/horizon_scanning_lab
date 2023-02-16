# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 09:18:33 2023

@author: Ravit
"""

import pandas as pd


# The df  was filtered first with abstracts bertopic and now with titles bertopic
# In[]
main_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\alon_filtered_files\arxiv_etn_eit_scidaily_sample_bertopic_abstract_filtered.csv')
filter_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\alon_filtered_files\title_bertopic_clusetrs_id_filtered.csv') 

# In[]
filter_df = filter_df[filter_df['rel']==1]
# In[]
filtered_topics = filter_df['Topic'].to_list()
# In[ ]
title_bertopics = main_df['title_bertopic_id'].to_list()
# In[]
keep_idx = []

for i, title_id in enumerate(title_bertopics):
    if title_id in filtered_topics:
        keep_idx.append(i)
        
new_df = main_df.iloc[keep_idx]

# In[]

new_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\alon_filtered_files\arxiv_etn_eit_scidaily_sample_bertopic_title_filtered.csv')

