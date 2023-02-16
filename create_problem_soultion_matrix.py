# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:32:47 2023

@author: Ravit
"""

import pandas as pd
from newspaper import Article

# In[]
df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\working_files\duplicate_filtered_files.csv')

# In[]
# extract urls via dois
doi_list = df['doi'].to_list()
url_list = []

for doi in doi_list:
    doi = doi.strip(' "doi":')
    url_list.append("https://doi.org/" + doi) 
# In[]
article_name = Article(url_list[0], language="en")

