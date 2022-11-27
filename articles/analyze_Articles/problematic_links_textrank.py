#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import os
import pandas as pd
import spacy
import plotly.express as px
import numpy as np
import pytextrank
import ssl
from bs4 import BeautifulSoup
from collections import Counter

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


# In[3]:


#For ignoring SSL ceritficate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# In[4]:


class infine_scroll(object): 
  def __init__(self, last):
    self.last = last

  def __call__(self, driver):
    new = driver.execute_script('return document.body.scrollHeight')  
    if new > self.last:
        return new
    else:
        return False


# In[5]:



def get_html_from_url(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  browser = webdriver.Chrome('C:\Program Files\chromedriver_win32 (1)\chromedriver', options=chrome_options) 
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


# In[6]:


# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")


# In[ ]:





# In[7]:


prob_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_articles_analysis\reddit_problematic_articles.txt", sep=" ")


# In[8]:


prob_df = prob_df.T


# In[9]:


prob_urls = prob_df.index.to_list()


# In[10]:


for i, url in enumerate(prob_urls):
    prob_urls[i] = url.split('"')[0].strip(',').strip('[').strip(']').replace("'","")


# In[11]:


prob_urls


# In[13]:


#get websites. This is to learn what parsing tags are required to extract text

websites = []
for url in prob_urls:
    websites.append(url.split('/')[2])


# In[14]:


websites = list(set(websites))


# In[15]:


def analyze_text_textrank(doc, rank_threshold=0.0):
    # examine the top-ranked phrases in the document
    rank_d = {"text":[], "rank":[], "count":[]}

    for phrase in doc._.phrases:
        if phrase.rank >= rank_threshold:
            rank_d['text'].append(phrase.text)
            rank_d['rank'].append(phrase.rank)
            rank_d['count'].append(phrase.count)
    
    return rank_d 


# Find parsers
# 

# 'siliconangle.com'
# title = soup.find('h3', {'class': 'sa-post-title'}).text
# body = soup.find('div', {'class': 'single-post-content'}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 
# 'www.newsweek.com' 
# title =  soup.find('h1', {'class':'title'}).text
# body = soup.find('div', {'class':'article-body v_text'}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 'www.thegamer.com'
# title = soup.find('h1', {'class':'heading_title'}).text
# body = soup.find('section', {'id':'article-body'}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 'apnews.com'
# title = soup.find('h1', {"class":"Component-heading-0-2-16"}).text
# body = soup.find('div', {"class":"Article"}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 'www.techdirt.com'
# #didn't succeed
# 
# 'agupubs.onlinelibrary.wiley.com'
# #didn't succeed
# 
# 'www.uq.edu.au'
# title = soup.find('h1', {'id':"page-title"}).text
# body = soup.find('div', {'id':"content"}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 'www.fiercebiotech.com'
# #didn't succeed
# 
# academic.oup.com
# #didn't succeed
# 
# www.science.org
# #didn't succeed
# 
# www.wsj.com
# title = soup.find('h1', {"class":"css-1lvqw7f-StyledHeadline e1ipbpvp0"}).text
# text = soup.find('section', {'class':'css-az2xkl-Container-Container e1d75se20'}).text
# 
# ww.tandfonline.com
# title = soup.find("span", {"class":"NLM_article-title hlFld-title"}).text
# text = soup.find("div", {"class":"abstractSection abstractInFull"}).text
# 
# www.abc.net.au
# title = soup.find("h1", {"class":"_1EAJU hMmqO WL4Yr n-Wqw _18EFj _2ZOIT _3HiTE x9R1x pDrMR hmFfs _390V1"}).text
# body = soup.find("div", {"class":"_3P3cP _3sFAh"}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# onlinelibrary.wiley.com
# #didn't succeed
# 
# 'www.sciencedirect.com'
# #didn't succeed
# 
# www.autoevolution.com
# #didn't succeed
# 
# www.pnas.org
# #didn't succeed
# 
# www.tomshardware.com
# title=soup.find("title").text
# body = soup.find("div",{"id":"article-body"})
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# thehill.com
# title=soup.find("title").text
# body = soup.find("div", {"class":"article__text | body-copy | flow"}).find_all('p')
# text = "".join([p.find_next(text=True).strip() for p in body])
# 
# 
# 
# journals.sagepub.com
# #not working
# 
# www.lightreading.com
# #not working
# 

# In[16]:


#websites that work with requests
requests_webs = ['siliconangle.com', 'www.newsweek.com', 'www.thegamer.com',  'apnews.com', 'www.uq.edu.au', 'www.wsj.com', 
'www.tandfonline.com', 'www.abc.net.au', 'www.tomshardware.com', 'thehill.com']

#websites that don't
no_requests_webs = ['www.techdirt.com', 'agupubs.onlinelibrary.wiley.com', 'www.fiercebiotech.com', 'academic.oup.com', 'www.science.org', 'onlinelibrary.wiley.com', 'www.sciencedirect.com', 'www.autoevolution.com', 'www.pnas.org', 'journals.sagepub.com', 'www.lightreading.com']

#doi.org => link not extracted properly
#remove from list
prob_urls.remove('https://doi.org/10.1016/j.humov.2022.103016')


# In[17]:


request_urls = [url for url in prob_urls if url.split('/')[2] in requests_webs]
still_prob_links = [url for url in prob_urls if url.split('/')[2] in no_requests_webs]


# In[18]:


soup = BeautifulSoup(request_urls[3])


# In[24]:


soup.text


# In[34]:


cols_title_df = ['article_keywords', 'title_keywords', 'count']
title_df = pd.DataFrame([], columns=cols_title_df)

cols_text_df = ['sentence', 'sentence_rank', 'count']
text_df = pd.DataFrame([], columns=cols_text_df)


# In[25]:


threshold_rank =0.05

for i, url in enumerate(request_urls):
    print(i)
    web = url.split('/')[2] 
    if web in requests_webs:
        try:
            result = get_html_from_url(url)
        except:
            print("url crashed")
            still_prob_links.append(url)
     
        soup = BeautifulSoup(result)
        if soup is None:
            still_prob_links.append(url)
            continue

        if web == 'siliconangle.com':
            try:
                title = soup.find('h3', {'class': 'sa-post-title'}).text
                body = soup.find('div', {'class': 'single-post-content'}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)


        if web=='www.newsweek.com':
            try:
                title =  soup.find('h1', {'class':'title'}).text
                body = soup.find('div', {'class':'article-body v_text'}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)
        
        if web=='www.thegamer.com':
            try:
                title = soup.find('h1', {'class':'heading_title'}).text
                body = soup.find('section', {'id':'article-body'}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)
            
        if web=='apnews.com':
            try:
                title = soup.find('h1', {"class":"Component-heading-0-2-16"}).text
                body = soup.find('div', {"class":"Article"}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)

        if web=='www.uq.edu.au':
            try:
                title = soup.find('h1', {'id':"page-title"}).text
                body = soup.find('div', {'id':"content"}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)
        if web=='www.wsj.com':
            try:
                title = soup.find('h1', {"class":"css-1lvqw7f-StyledHeadline e1ipbpvp0"}).text
                text = soup.find('section', {'class':'css-az2xkl-Container-Container e1d75se20'}).text
            except:
                still_prob_links.append(url)
        if web=='www.tandfonline.com':
            try:
                title = soup.find("span", {"class":"NLM_article-title hlFld-title"}).text
                text = soup.find("div", {"class":"abstractSection abstractInFull"}).text
            except:
                still_prob_links.append(url)
        if web=='www.abc.net.au':
            try:
                title = soup.find("h1", {"class":"_1EAJU hMmqO WL4Yr n-Wqw _18EFj _2ZOIT _3HiTE x9R1x pDrMR hmFfs _390V1"}).text
                body = soup.find("div", {"class":"_3P3cP _3sFAh"}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)
            
        if web=='www.tomshardware.com':
            try:
                title=soup.find("title").text
                body = soup.find("div",{"id":"article-body"})
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)
        
        if web == 'thehill.com':
            try:
                title=soup.find("title").text
                body = soup.find("div", {"class":"article__text | body-copy | flow"}).find_all('p')
                text = "".join([p.find_next(text=True).strip() for p in body])
            except:
                still_prob_links.append(url)

        text_doc = nlp(text)
        title_doc = nlp(title)

        text_dict = analyze_text_textrank(text_doc, threshold_rank)
        title_dict = analyze_text_textrank(title_doc, threshold_rank)

        temp_text_df = pd.DataFrame.from_dict(text_dict)
        temp_text_df.columns = cols_text_df
        temp_text_df['article_link'] = [url]*len(temp_text_df)
        text_df = pd.concat([text_df, temp_text_df])
 
        temp_title_df = pd.DataFrame.from_dict(title_dict)
        temp_title_df.columns = cols_title_df
        temp_title_df['article_link'] = [url]*len(temp_title_df)
        title_df = pd.concat([title_df, temp_title_df])
        


# In[ ]:


title_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_articles_analysis\problematic_reddit_articles_titles.csv")
text_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_articles_analysis\problematic_reddit_articles_texts.csv")

#save questions that selenium didn't succeed either
stubborn_df = pd.DataFrame(still_prob_links, columns=['url'])
stubborn_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_articles_analysis\prob_articles_after_second_try.csv")

