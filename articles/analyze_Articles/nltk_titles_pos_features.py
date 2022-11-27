# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:06:55 2022

@author: Ravit
"""

# In[0]
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from collections import Counter
import pandas as pd
import numpy as np
# In[1]
feature_names = ['for', 'can', 'could', 'use', 'will', 'sum_verbs', 'RB', 
                  'RBR', 'RBS', 'VB', 'VBG', 'VBP', 'VBZ', 'JJ'] 



def create_pos_features_per_title(title):
    py_sword = set (stopwords.words ('english'))
    py_token = sent_tokenize(title)
   
    new_row = pd.DataFrame(np.zeros((1,len(feature_names))), columns=feature_names )
    Names_list = []

    for sentence in py_token:
        py_lword = nltk.word_tokenize(sentence)
        #search for only capitel latters names like crispr
        for i, w in enumerate(py_lword):
            if w.lower() in py_sword:
                continue
            if w.isalpha() is False:
                continue
            if w == w.upper():
                Names_list.append(w)
                continue
            if (w[0] == w[0].upper()) and (i!=0):
                Names_list.append(w)

        py_tag = nltk.pos_tag(py_lword)
        all_tokens = [t[1] for t in py_tag]
        count_tokens = Counter(all_tokens)       
    
        verb_tags = ['VB', 'VBG', 'VBP', 'VBZ']
        for verb_tag in verb_tags:
            new_row['sum_verbs']  += count_tokens[verb_tag]
            new_row[verb_tag] = count_tokens[verb_tag]

        if 'for' in py_lword:
            new_row['for'] +=1
        if 'can' in py_lword:
            new_row['can'] +=1
        if 'could' in py_lword:
            new_row['could'] +=1
        if 'will' in py_lword:
            new_row['will'] +=1
        if 'use' in py_lword:
            new_row['use'] +=1

    if Names_list == []:
        Names_list = [None]

        
    new_row['Names'] = [Names_list]
    return new_row
# In[2]
df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
title_list = df['titles'].to_list()
link_list = df['link'].to_list()
# In[3]
 
out_df = pd.DataFrame([], columns=feature_names)

for i, title in enumerate(title_list):
    df_row = create_pos_features_per_title(title)    
    out_df = pd.concat([out_df, df_row], axis=0)
    
out_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\extracted_POS.csv")

 
