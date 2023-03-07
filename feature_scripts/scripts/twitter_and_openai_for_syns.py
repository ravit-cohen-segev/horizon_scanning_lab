# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 21:39:26 2023

@author: Ravit
"""


import os
import tweepy
import pandas as pd
import json
from dotenv import load_dotenv

os.chdir(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\scripts')
from open_AI_GPT import *

# In[]
# 1. use twitter API to extract tweets with technology key word  

load_dotenv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\twitter_RCS\.env')
consumer_key = os.environ["API_KEY"]
consumer_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(consumer_key, 
  consumer_secret
)


api = tweepy.API(auth)


def extract_tweets(query):
    all_hashtags = []
    all_texts = []
    tweets = api.search_tweets(q=query)

    for tweet in tweets:
        all_hashtags.append([tag['text'] for tag in tweet.entities['hashtags']])
        all_texts.append(tweet.text)
    assert(len(all_hashtags) == len(all_texts))        
    
    return all_texts, all_hashtags


# In[]

openai.api_key = os.getenv("OPENAI_API_KEY")
with open(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\output_htmls\13Feb23_new_sites_html_text.json") as f:
    dict_htmls = json.loads(f.read())

with open(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\output_pdfs\13Feb23_arxiv_pdf_text.json") as f:
    dict_pdfs = json.loads(f.read())
    

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\alon_files_after_clusteirng\7March2023_merged_Levi_dfs_with_index.csv')

tech_names = df['Tech_Name'].to_list()


# In[]
tech_syns = pd.DataFrame([], columns = ['hashtags', 'openAI_tech_in_tweets'])

for tech in tech_names:
    all_texts, all_hashtags = extract_tweets(tech)
    all_hashtags = [hashtag for hashtag in all_hashtags if hashtag!=[]]
    
