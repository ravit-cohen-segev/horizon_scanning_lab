# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:29:41 2023

@author: Ravit
"""

import pandas as pd
import numpy as np 
import requests
import re
import os
import time
import codecs

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# In[]

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

# In[]
domains_articles = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\arxiv_etn_eit_scidaily_sample.csv')
# In[]

arxiv_articles = domains_articles[domains_articles['source'] == 'arxiv']


scidaily_articles = domains_articles[domains_articles['source'] == 'science_daily']


# In[]

arxiv_id = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\arxiv_smaple_with_id.csv')

doi_list = arxiv_id['doi'].to_list()
doi_idx= []

for i, doi in enumerate(doi_list):
    if doi is np.nan:
        continue
    if '10.' in doi:
        doi_idx.append(i)
        
arxiv_id = arxiv_id.iloc[doi_idx]

# In[]
titles = arxiv_articles['title'].to_list()

# In[]

df = pd.concat([arxiv_articles, scidaily_articles], axis=0)


# In[]
# get list of citations with list of DOI. This eas done manually with the web app https://timwoelfle.github.io/Local-Citation-Network/
# There's no way to download the table so I saved the html page for parsing

file = codecs.open(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\arxiv_html.txt", encoding='utf-8')

cite_html = BeautifulSoup(file.read())


all_cells = cite_html.find('table').find_all('div', {'class':'tooltip-trigger'})

all_cells = [cell.text.replace('\r','').replace('\n','').replace('  ','') for cell in all_cells]



all_cells = pd.DataFrame(np.array(all_cells).reshape(int(len(all_cells)/6), 6))
# In[]
all_top_citations = cite_html.find_all('div', {'class':'table-wrapper has-mobile-cards'})[1].find_all('div', {'class':'tooltip-trigger'})

all_top_citations = [top.text.replace('\r','').replace('\n','').replace('  ','') for top in all_top_citations][5:]

all_top_citations = pd.DataFrame(np.array(all_top_citations).reshape(int(len(all_top_citations)/6), 6))


# In[]
new_header = all_cells.iloc[0] #grab the first row for the header
all_cells = all_cells[1:] #take the data less the header row
all_cells.columns = new_header #set the header row as the df header
all_top_citations.columns = new_header


# In[]

titles = cite_html.find_all('td', {'data-label':'Title'})
titles = [title.text.replace('\r','').replace('\n','') for title in titles]

top_titles = titles[-10:]
titles = titles[:-10]

all_cells['title'] = titles
all_top_citations['title'] = top_titles
# In[]

merged = pd.merge(all_cells, arxiv_id, on='title')

merged['Cit'] = pd.to_numeric(merged['Cit'])

merged_sorted = merged.sort_values(by='Cit', ascending=False)

merged_sorted.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\arxiv_articles_with_citation_count.csv')

# In[]
#do the same with scidaily
scidaily_df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\science_daily_RCS\docs\scrapped_latest_scidaily_articles_with_doi.csv')

# In[]
sci_file = codecs.open(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\sci_daily_html.txt", encoding='utf-8')

sci_cite_html = BeautifulSoup(sci_file.read())


sci_all_cells = sci_cite_html.find('table').find_all('div', {'class':'tooltip-trigger'})

sci_all_cells = [cell.text.replace('\r','').replace('\n','').replace('  ','') for cell in sci_all_cells]


sci_all_cells = pd.DataFrame(np.array(sci_all_cells).reshape(int(len(sci_all_cells)/6), 6))
# In[]



# In[]
new_header = sci_all_cells.iloc[0] #grab the first row for the header
sci_all_cells = sci_all_cells[1:] #take the data less the header row
sci_all_cells.columns = new_header #set the header row as the df header

# In[]
sci_titles = sci_cite_html.find_all('td', {'data-label':'Title'})
sci_titles = [title.text.replace('\r','').replace('\n','') for title in sci_titles]

sci_all_cells['title'] = sci_titles[:-1]
# In[]
sci_merged = pd.merge(sci_all_cells, scidaily_df, on='title')

sci_merged['Cit'] = pd.to_numeric(sci_merged['Cit'])

sci_merged_sorted = sci_merged.sort_values(by='Cit', ascending=False)

sci_merged_sorted.drop(['Unnamed: 0','Unnamed: 0.1'], axis=1, inplace=True)

# In[]:
sci_merged_sorted.drop_duplicates(inplace=True)
sci_merged_sorted.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\scidaily_with_citation_count.csv')