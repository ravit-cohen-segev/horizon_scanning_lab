#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import spacy
import pytextrank

import pandas as pd
import glob
import os
from tqdm import tqdm

from collections import Counter

import itertools

import string
import numpy as np


# In[9]:


allowed = set(string.ascii_lowercase + string.ascii_uppercase+ string.digits + "'")

import re

s="elon musk"

print(bool(re.match('^[a-zA-Z0-9]+$', s)))


# In[10]:


stop_words = set(stopwords.words('english'))


# In[11]:

nlp = spacy.load('en_core_web_lg')


# In[12]:


df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\24Jan2023_all_domains_with_reddit_crunch.csv").set_index(['Unnamed: 0'])



# In[13]:

BAD_DEP=["poss","det"]
ALLOWED_ENT = ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "CARDINAL"]

def filter_sentence(sent):
    doc = nlp(sent)
    filtered_sentence=[]
    for noun_chunk in doc.noun_chunks:
        original_chunk=noun_chunk
        if noun_chunk[0].dep_ in BAD_DEP:
            noun_chunk=noun_chunk[1:]
        
        w=noun_chunk.text.lower()
        ent=noun_chunk.root.ent_type_
        if ent not in ALLOWED_ENT:
            continue
        w=noun_chunk.text.lower()
#         if w not in stop_words:
        # if check(w):
        #     print(w)
        
        filtered_sentence.append({"word":w,
                                      "entity":noun_chunk.root.ent_type_,
                                      "dependency":noun_chunk.root.dep_,
                                     "original_word":original_chunk.text})
            

    return filtered_sentence
print(filter_sentence("Enhancing Cellular Communications for UAVs via Intelligent Reflective  Surface"))


# In[16]:


words_abs=[]
words_title=[]
abstract_index = []
abstract_index = []


for index, row in df.iterrows():
    abstract=row["abstract"]
   # title=row["title"]
    filtered = filter_sentence(abstract)
    words_abs += filtered

    abstract_index.extend([row['source']+str(index)]*len(filtered))
    #words_title += filter_sentence(title)
    
    
# In[]
df_abs = pd.DataFrame(np.empty((0, 4)), columns=["word", "entity", "dependency","original_word"]) 

for i,item in enumerate(words_abs):
    item_df = pd.DataFrame(item, index=[i])
    df_abs = pd.concat([df_abs, item_df]) 
df_abs['abstract_index'] = abstract_index

# In[]
df_abs.set_index(['abstract_index'], inplace=True)
df_abs.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\combined_domains\docs\with_reddit_crunch\docs\2Feb23_abstract_entities.csv')

# In[]
# Nehoray's code
'''
df_abs=pd.DataFrame(words_abs)
df_abs["count"] = 1
df_abs = df_abs.groupby(["word", "entity", "dependency","original_word"])["count"].count().reset_index()
df_abs["len"]=df_abs["word"].str.count(' ') + 1
#df_abs.to_excel("")

'''
# In[18]:
'''

df_abs["entity"].value_counts()
'''
