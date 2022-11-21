# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:28:04 2022

@author: Ravit
"""

import numpy as np
import pandas as pd

import en_core_web_sm
import os
from nltk.corpus import wordnet
from yellowbrick.cluster import KElbowVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
# In[0]
folder_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic"
original_path = os.path.join(folder_path,"extracted_verbs_nouns_before_bertopic.csv")

original_df = pd.read_csv(original_path)

no_verbs_set_aside = original_df[original_df['spacy_verbs'].isna()]
original_df = original_df[~original_df['spacy_verbs'].isna()]

# In[1]
def create_synonyms_wordnet(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return list(set(synonyms))
# In[2]
def create_verb_bag_of_words(verb_str):
    if verb_str is np.nan:
        return ['']
    list_verbs = verb_str.split()
    synonyms = ['']
    for w in list_verbs:
        synonyms += [syn.lower() for syn in create_synonyms_wordnet(w)]
    return list(set(synonyms))

nlp = en_core_web_sm.load()

def spacy_tokenizer(document):
    tokens = nlp(document)
    tokens = [token.lemma_ for token in tokens if (
        token.is_stop == False and \
        token.is_punct == False and \
        token.lemma_.strip()!= '')]
    return tokens


# In[3]
spacy_verbs_list = original_df['spacy_verbs'].to_list()

nltk_syn_list = []

for i, sentence in enumerate(spacy_verbs_list):
    nltk_syn_list.append(" " .join(create_verb_bag_of_words(sentence)))
# In[4]
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english', tokenizer=spacy_tokenizer)
X = vectorizer.fit_transform(nltk_syn_list)
features = vectorizer.get_feature_names_out()
transformed_documents_as_array = X.toarray()

# In[5]
np.random.seed(0)
km = KMeans()
title_visualizer = KElbowVisualizer(km, k=(2,10), random_state=0)

title_visualizer.fit(transformed_documents_as_array)
title_visualizer.show() 
# In[6]
kmeans = KMeans(n_clusters=5).fit(transformed_documents_as_array)
labels = list(kmeans.labels_)
#add unknown labels to titles without verbs
labels.extend([np.nan]*len(no_verbs_set_aside))
new_df = pd.concat([original_df, no_verbs_set_aside], axis=0)
new_df['label'] = labels 

new_df.drop(['spacy_nouns'], axis=1, inplace=True)
new_df.sort_values(by='label', inplace=True)

new_df.to_csv("clustered_verbs_synonyms.csv")
