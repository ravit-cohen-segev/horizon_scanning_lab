# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:13:28 2022

@author: Ravit
"""

import pandas as pd
import re


def remove_ascii_chars(text):
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    return text 

def remove_punc(text):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    text.replace(punc, ' ')
   # text = "".join([t for t in text if t not in punc])
    return text

def separate_two_sentences(text):
    words = text.split()
    #perserve names like NYC
    perserve_names = [w for i, w in enumerate(words) if (len(w)>1) and (w == w.upper()) ]
    text = re.findall('[a-zA-Z][^A-Z]*', text)
    new_text = " ".join(text)
    
    for perserve in perserve_names:
        new_text = new_text.replace(" ".join([l for l in perserve]), perserve)
    return new_text

def fix_texts(text_list):
    for i, txt in enumerate(text_list):
        txt = remove_ascii_chars(txt)
        txt = remove_punc(txt)
        txt = separate_two_sentences(txt)
        text_list[i] = txt
        return text_list
        

df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering.csv")

titles_list = fix_texts(df['titles'].to_list())
abstracts_list = fix_texts(df['abstract'].to_list())

new_df = df.copy()
new_df['titles'] = titles_list
new_df['abstract'] = abstracts_list
new_df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True) 
new_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")






