# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 13:06:26 2023

@author: Ravit
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import re
# In[]

#core_id = '84871977'
#title = 'Senza luoghi e senza alivi. La scrittura di Marisa Madieri'
df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\core_parsed_files\20Nov2023_filtered_articles_for_doi_retreival.csv')


# In[]
def query_api(search_url, query):
    response = requests.get(f"{search_url}?q={query}")
    return response

def find_doi_in_html(html):
  doi_match = re.search(r'<meta(?: [^>]+)? content="https?://doi.org/([^"]+)"', html)
  if doi_match:
    return doi_match.group(1)
  
  text_doi_match = re.search(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', html)
  if text_doi_match:
    return text_doi_match.group(0)

  return None


def find_doi(text, title):
    soup = BeautifulSoup(response.text)
    json_ = soup.find('script', {"id": "__NEXT_DATA__"})
    d = json.loads(json_.text)
    d = d['props']['pageProps']['data']['results']
    
    for d_item in d:
        if d_item['doi'] is not None:
            
            if d_item['title'] == title:
                return d_item['doi']
    
    doi_pattern = re.compile(r'doi">(.*?)</') 

    return re.findall(doi_pattern, text)

# In[]

extracted_dois = ['None']*len(df)

for i, row in df.iterrows():
    core_id = row['coreId']
    response= query_api("https://core.ac.uk/search", core_id)
    extracted_dois[i] = find_doi_in_html(response.text)
    doi_tags = find_doi(response.text, row['title'])

    
# In[]
