# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:54:41 2023

@author: Ravit
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import spacy
import pytextrank
from PyPDF2 import PdfReader

import pandas as pd
from collections import Counter
# In[]
example = 'Improvements in rechargeable batteries are enabling several electric urban air mobility (UAM) aircraft designs with up to 300 miles of range with payload equivalents \
    of up to 7 passengers. We find that novel UAM aircraft consume between 130 Wh/passenger-mile up to ~1,200 Wh/passenger-mile depending on the\
    design and utilization, relative to an expected consumption of over 220 Wh/passenger-mi for terrestrial electric vehicles and 1,000 Wh/passenger-mile\
    for combustion engine vehicles. We also find that several UAM aircraft designs are approaching technological viability with current Li-ion batteries, based on\
    the specific power-and-energy while rechargeability and lifetime performance remain uncertain. These aspects highlight the technological readiness of a new segment of transportation.'
# In[]
# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
    
# In[]

stop_words =  stopwords.words("english")
lemmatizer = WordNetLemmatizer()

word_tokenized = word_tokenize(example)



without_stop_words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenized if not word in stop_words and word.isalpha()]
print(Counter(without_stop_words).most_common())

# In[] 
doc = nlp(example.lower())
dfs_abstract = pd.DataFrame([], columns=['text', 'rank', 'count'])

# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    dfs_abstract = pd.concat([dfs_abstract, pd.DataFrame([[phrase.text, phrase.rank, phrase.count]], columns = dfs_abstract.columns)]) 
    
# In[]

# creating a pdf reader object
reader = PdfReader(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\example_article_for_scrapping_sentence_features.pdf')

i = 0 
cont_flag = True

parts = []
while cont_flag:

    try:
        page = reader.pages[i]
    except:
        cont_flag=False
        break

    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720:
            parts.append(text)


    page.extract_text(visitor_text=visitor_body)
    
    i +=1
    
text_body = "".join(parts)

print(text_body)


print(page.extract_text())


# In[]
doc = nlp(text_body.lower())
dfs_article = pd.DataFrame([], columns=['text', 'rank', 'count'])

# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    dfs_article = pd.concat([dfs_article, pd.DataFrame([[phrase.text, phrase.rank, phrase.count]], columns = dfs_article.columns)]) 
    
# In[]
example = ""
    