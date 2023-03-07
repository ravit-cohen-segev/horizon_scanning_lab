# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 08:29:51 2023

@author: Ravit
"""

from newspaper import Article
import pandas as pd
import time
import csv
import json
import re
# In[]:

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv').set_index(['Unnamed: 0'])

df_without_arxiv = df[df['source']!='arxiv']

# In[]
d = {}


for index, row in df_without_arxiv.iterrows():
    url = row['link']    
    article = Article(url)
   
    try:
        article.download() 
           
        d[index] = re.sub("\s+", " ", article.text)
    except:
        continue
 
    time.sleep(2)

# In[]
f = open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\output_htmls\13Feb23_new_sites_html_text.json', 'w')

f.write(json.dumps(d))

