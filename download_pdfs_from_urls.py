# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:05:03 2023

@author: Ravit
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article

import re
import os

# In[]

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



# In[]
def download_pdf(url, folder_path, file_name):

    # Send GET request
    response = requests.get(url, headers=hdr)

    # Save the PDF
    
    full_path = os.path.join(folder_path, url.split("/")[-1] )
    with open(full_path, "wb") as f:
      f.write(response.content)
    return response.content

def download_html(url, folder_path, file_name):
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    if len(text) == 0:
        response = requests.get(url)
        text = re.sub(r"\s+", "", BeautifulSoup(response.content).text)
        
    full_path = os.path.join(folder_path, file_name+'.txt')
    with open(full_path, "w") as f:
      f.write(text)
    return text
    
    
# In[]

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\usda\docs\working_files\12Feb23_usda_crossref_features.csv').set_index('Unnamed: 0')
pdf_folder_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\docs\out_pdfs'
html_folder_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\docs\out_htmls'

df_pdf_index = pd.DataFrame([], columns=['pdf_file_name'])
pdf_file_names = []
pdf_file_index = []

for index, row in df.iterrows():
    url = row['pdf_link']
    
    if url != 'UNKNOWN':
        file_name = url.split("/")[-1]
        pdf = download_pdf(url= url, folder_path=pdf_folder_path, file_name = file_name) 
        if pdf is not None:
            pdf_file_index.append(index)
            pdf_file_names.append(file_name)
    else:
        url = row['URL']
        try:
            text = download_html(url, folder_path=html_folder_path, file_name=index)
        except:
            print('unable to extract text from ', url)
            
            
df_pdf_index['pdf_file_name'] = pdf_file_names
df_pdf_index.index = pdf_file_index

# In[]
df_pdf_index.to_csv(os.path.join(pdf_folder_path, 'table_index.csv'))
 
