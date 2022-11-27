# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:48:48 2022

@author: Ravit
"""

import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan

# In[0]:

ans_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\abstracts_full_final.csv"
abstracts_df = pd.read_csv(ans_path)

# In[1]
# remove rows with no abstracts
abstracts_df = abstracts_df[abstracts_df['abstract'] != '[]']
abstracts_list = abstracts_df['abstract'].to_list()

# In[2]
# analyze with tf-idf nltk an example
text = abstracts_list[0]
sentences = sent_tokenize(text)  # NLTK function
total_documents = len(sentences)

# In[3]

def get_tf_idf_features(sentence):
    vectorizer = TfidfVectorizer(token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', 
                             stop_words=set(stopwords.words("english")))
    X = vectorizer.fit_transform(sentences)
    return vectorizer.get_feature_names()


# In[4]





 
