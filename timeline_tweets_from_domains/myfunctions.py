# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:51:54 2023

@author: Ravit
"""

import pandas as pd
import numpy as  np
import re
import ssl
import json
import os
import itertools
from tqdm import tqdm

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta, date
import calendar
from collections import OrderedDict, Counter
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# In[]
def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def remove_tabs_spaces(elements):
    '''{input: a list of text elments
    output: list of parsed elements }'''
    return [" ".join(remove_non_ascii(el).replace('\n', ' ').replace('\t', '').split()) for el in elements]

def remove_sparse_features(df, threshold=0.01):
    variance = df.var()
    drop_cols = []
    for col in df.columns:
        if variance[col]<threshold:
            drop_cols.append(col)
    return df.drop(drop_cols, axis=1)


def read_csv_into_chunks(path, chunks=5):
    dfs = pd.read_csv(path, chunksize=chunks)
    return pd.concat(dfs)

# In[]
#For ignoring SSL ceritficate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class infine_scroll(object): 
  def __init__(self, last):
    self.last = last

  def __call__(self, driver):
    new = driver.execute_script('return document.body.scrollHeight')  
    if new > self.last:
        return new
    else:
        return False


def get_html_from_url(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  browser = webdriver.Chrome(options=chrome_options) 
  browser.get("http://www.python.org")
  assert "Python" in browser.title
  browser.set_page_load_timeout(30) 
  browser.get(url)
   
  last_height = browser.execute_script('return document.body.scrollHeight')

  flag=1
  
  while flag==1:
    
    try:
       browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
       wait = WebDriverWait(browser, 10)

       new_height = wait.until(infine_scroll(last_height))
       last_height = new_height

    except:
        flag = 0
    
  html = browser.page_source
  return html


# In[]
start_date = "2015-01-01"
end_date = "2023-02-28"

dates = [start_date, end_date]

def create_empty_timeseries_df_with_tech_names(tech_names):
    '''{input: tech list, articles from a certain domain 
    output: empty df for counting number of mention in news}'''

    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    month_list = [i.strftime("%b-%y") for i in pd.date_range(start=start_date, end=end_date, freq='MS')]


    df = pd.DataFrame(np.zeros((len(tech_names), len(month_list))), columns = month_list)
    df.index = tech_names
 
    return df
    
# In[]

def create_tech_list_timeseries_news_titles_techcrunch(dict_tech_names, domain_df):
    '''{input: dict with techs and synonyms
    output: df with news from a specific domain}'''
    
    df_counts = create_empty_timeseries_df_with_tech_names(dict_tech_names.keys(), domain_df)
    
    for i, row in domain_df.iterrows():
        title = row['title'].lower()
        date = row['date'].split('•')[1]
        date_split = date.split()
        date_split[0] = date_split[0][:3]
        date_str = "-".join([date_split[0], date_split[2][-2:]])
                
        for key in dict_tech_names.keys():
            syns_list = [key] + dict_tech_names[key]
            for syn in syns_list:
                if syn.lower() in title:
                    try:
                        df_counts.loc[key][date_str] += 1
                        break
                    except:
                        print(date_str + ' not in requested dates')
    return df_counts
                        
                    
# In[]
#TODO COMPLETE
def create_tech_list_timeseries_news_titles_NYT(tech_syns, domain_dfs_path):
    # concat all separate NYT csv files into one
    file_names = os.listdir(domain_dfs_path)
    
    df_counts = create_empty_timeseries_df_with_tech_names(tech_syns.index)
    
    dfs = pd.DataFrame([]) 
    
    for file in file_names:
        file_path = os.path.join(domain_dfs_path, file)
        df = pd.read_csv(file_path)
        df['pub_date'] = pd.to_datetime(df['pub_date'])
        
        dfs = pd.concat([dfs, df])
        
    #convert dates                
    dates_list = dfs['pub_date'].to_list()
    dates_list = [calendar.month_abbr[date.month] + '-' + str(date.year)[-2:] for date in dates_list]
    dfs['pub_date'] = dates_list
    
    #remove rows with no text
    dfs = dfs[dfs['abstract'].notna()]
    
    all_mentioned_techs = []
    
    for i, row in dfs.iterrows():     
        date_col = row['pub_date']
        text = row['abstract']
        mentioned_techs = []
        
        for tech, tech_row  in tech_syns.iterrows():
            row_syns = list(set([tech] +  tech_row.dropna().to_list()))
            
            for syn in row_syns:
                if syn == syn.upper():
                    #syn is acronym
                    syn = ' ' + syn + ' '
                    if syn in text:
                        mentioned_techs += [tech]
                                    
                else:
                    syn = syn.lower()
                    if syn in text.lower():
                        mentioned_techs += [tech]
    
    dfs['mentioned_techs'] = all_mentioned_techs 
    
    for date in search_dates:
        temp_df = dfs[dfs['date']==date]
        date_techs = temp_df['mentioned_techs'].to_list()
        count_techs = Counter(list(itertools.chain.from_iterable(date_techs)))
        
        for key in count_techs.keys():
            df_counts.loc[key][date] = count_techs[key]
    
    
     
    return df_counts


# In[]

class time_series_tech_tweets():
    def __init__(self, tech_syns, start_date = "2015-01-01", end_date = "2023-02-28"):
        self.start_date = start_date
        self.end_date = end_date
        self.tech_syns = tech_syns
    

    def create_empty_df_counts(self):
        '''{input: tech list, articles from a certain domain 
        output: empty df for counting number of mention in news}'''
    

        dates = [self.start_date, self.end_date]
        tech_names = self.tech_syns.index
    
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        month_list = [i.strftime("%b-%y") for i in pd.date_range(start=self.start_date, end=self.end_date, freq='MS')]


        df_counts = pd.DataFrame(np.zeros((len(tech_names), len(month_list))), columns = month_list)
        df_counts.index = tech_names
        return df_counts
     
    
    def create_date_list(self,  dfs, date_col):
        dates_list = dfs[date_col].to_list()
        dates_list = [date.replace('Published: ', '').replace('Last Updated: ', '').replace('  ','').replace('/n', '').replace('|', '') for date in dates_list]
        return dates_list

    def count_techs_in_text_tn(self, tn_path, date_col='date'):
        #read all csv files and concat into 1
        tn_files = os.listdir(tn_path)
        dfs = pd.concat([pd.read_csv(os.path.join(tn_path,file)) for file in tn_files])
        dates_list = self.create_date_list(dfs, date_col)
        
        for i, date in enumerate(dates_list):
            try:
                dfs[date_col].iloc[i] = pd.to_datetime(date).strftime("%b-%y")
            except:
                date_split = list(set(dates_list[i].split()))
                month = ''
                year = ''
                for d in date_split:
                    if d.isalpha():
                        month = d
                    elif len(d)==4:
                        year = d
                dfs['date'].iloc[i] = pd.to_datetime('November' + ' ' + '2021').strftime("%b-%y")

        df_counts = self.create_empty_df_counts()
        
        #drop dates that don't exist in dataset
        search_dates = [col for col in df_counts.columns if col in dfs[date_col].to_list()]
        
        df_counts.drop([col for col in df_counts if col not in search_dates], axis=1, inplace=True)
        
        
        # what techs are in every article
        all_mentioned_techs = []
        
        for i, row in tqdm(dfs.iterrows()):
            title = row['title']
            summary = row['summary']
            mentioned_techs = []
            
            for tech, tech_row  in self.tech_syns.iterrows():

                row_syns = list(set([tech] +  tech_row.dropna().to_list()))
                for syn in row_syns:
                    
                    if syn == syn.upper():
                        #syn is acronym
                        syn = ' ' + syn + ' '
                        if (syn in title) or (syn in summary):
                            mentioned_techs += [tech]
                           
                        
                    else:
                        syn = syn.lower()
                        if ((syn in title.lower()) or (syn in summary.lower())):
                            mentioned_techs += [tech]
         
            all_mentioned_techs.append(mentioned_techs)      
        dfs['mentioned_techs'] = all_mentioned_techs 
        
        for date in search_dates:
            temp_df = dfs[dfs['date']==date]
            date_techs = temp_df['mentioned_techs'].to_list()
            count_techs = Counter(list(itertools.chain.from_iterable(date_techs)))
            
            for key in count_techs.keys():
                df_counts.loc[key][date] = count_techs[key]
        
        return df_counts
    
    
    def is_syn_in_text(self, syn_list, text):
        
        for syn in syn_list:
            if syn == syn.upper():
                #syn is acronym
                syn = ' ' + syn + ' '
                if syn in text:
                    return True
                
            else:
                syn = syn.lower()
                if syn in text.lower():
                    return True
        return False
        
    
    
    def count_techs_in_text_NYT(self, NYT_path, date_col=''):
        # read each csv. date and month is in file name
        file_names = os.listdir(NYT_path)
        
        df_counts = self.create_empty_df_counts()
        
        all_mentioned_techs = []
        
        for file in file_names:
            file_path = os.path.join(NYT_path, file)
            df = pd.read_csv(file_path)
            date_str = re.sub("[^0-9]", "", file)
            year, month = date_str[:4], date_str[4:]
            date = datetime.strptime(year +'-' +month, '%Y-%m')
            date = date.strftime("%b-%y")
            mentioned_techs = []
            
            # combine all texts from a month into one string
            # fix bad parsing while doing it
            abstracts = df['abstract'].to_list()
            
            
            abstracts = [remove_non_ascii(abstract) for abstract in abstracts if abstract is not None]
            
            for tech, tech_row in self.tech_syns.iterrows():
                syn_list = list(set([tech] +  tech_row.dropna().to_list()))
                
                for text in abstracts:
                    if self.is_syn_in_text:
                        df_counts.loc[tech][date] += 1
                        
        return df_counts
                        
# In[]

tech_syns = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\9March23_tech_synonyms_and_names - Sheet1.csv').set_index('Tech_Name')
NYT_path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\NYT_RCS\docs\headlines\csv_converted_files'

# In[]
NYT_counts = time_series_tech_tweets(tech_syns).count_techs_in_text_NYT(NYT_path)   
        
     