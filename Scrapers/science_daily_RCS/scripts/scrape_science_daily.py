# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 13:19:23 2023

@author: Ravit
"""

import urllib, urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd

# In[]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def extract_html(url):
    response = requests.get(url, headers=hdr)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def remove_tabs_spaces(text):
    return text.replace('\n', '').replace('\t', '')
# In[]

# get all topic_urlsto scrape from
topic_urls = []

url = 'https://www.sciencedaily.com/news/top/science/'

soup = extract_html(url)


sci_topics_box = soup.find('div', {'class':'col-xs-6 col-md-12'})

all_topics_boxes = sci_topics_box.find_all('li', {'class':'nav-header'})[1:]

for i, topic in enumerate(all_topics_boxes):

    topic_hrefs = topic.find_all('a')
    topic_hrefs = ['https://www.sciencedaily.com' + topic['href'] for topic in topic_hrefs if '/news/' in topic['href']]
    
    topic_urls.extend(topic_hrefs)

# In[]

def find_topic_news(link):
    soup = extract_html(link)
    news = soup.find_all('h3')
    news_titles = []
    news_links = []
    
    for new in news:
        try:
            news_links.append('https://www.sciencedaily.com' + new.find('a')['href'])
            news_titles.append(new.text)
        except:
            print('Couldnt detect a link')
     
    news_summaries = soup.find_all('div' , {'class':'latest-summary'})
    dates = [summary.find('span', {'class':'story-date'}).text for summary in news_summaries]
    summaries = [remove_tabs_spaces(summary.text.split(' — ')[1]) for summary in news_summaries]
    return dates, news_titles, summaries, news_links

# In[]
df = pd.DataFrame([], columns = ['date', 'title', 'summary', 'link','topic'])
all_titles = []
all_links = []
all_topics = []
all_dates = []
all_summaries = []

for url in topic_urls:
    topic = url.replace('https://www.sciencedaily.com/news', '').replace('/','')
    
    dates, titles, summaries, links = find_topic_news(url)
    
    all_dates.extend(dates)
    all_titles.extend(titles)
    all_summaries.extend(summaries)
    all_links.extend(links)
    all_topics.extend([topic]*len(titles))
    
df['date'] = all_dates
df['title'] = all_titles
df['summary'] = all_summaries
df['link'] = all_links
df['topic'] = all_topics 
# In[]
df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\science_daily_RCS\docs\scrapped_latest_scidaily_articles.csv')