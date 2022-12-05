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
from nltk.data import load

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np


# In[1]
#Two ways for making features:
#1. simple count of noun and verbs
#2. Sentence vector representation - taking into account the order of words 
'''
# In[2]
#1.
feature_names = ['for', 'can', 'could', 'use', 'will', 'sum_verbs', 'RB', 
                  'RBR', 'RBS', 'VB', 'VBG', 'VBP', 'VBZ', 'JJ'] 

def create_pos_features_per_title(title):
    py_sword = set(stopwords.words ('english'))
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
'''
# In[4]

df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
title_list = df['titles'].to_list()
link_list = df['link'].to_list()

# In[]
'''
title_lengths = [len(nltk.word_tokenize(title)) for title in title_list]
title_word_count = Counter(title_lengths)


# In[5]

out_df = pd.DataFrame([], columns=feature_names)

for i, title in enumerate(title_list):
    df_row = create_pos_features_per_title(title)    
    out_df = pd.concat([out_df, df_row], axis=0)
    
out_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\extracted_POS.csv")
'''
# In[6]

#2.  
tagdict = load('help/tagsets/upenn_tagset.pickle')

# In[7]
#for ordianl features

#ordinal_features = np.array(['None'] + list(tagdict.keys()))
ordinal_features = np.array(list(tagdict.keys()))

max_len = 24

def sentence_vector_space(sentence):
    word_tags = nltk.pos_tag(nltk.word_tokenize(sentence))
    vector_sen = []
    
    for i, (word, tag) in enumerate(word_tags):
        vector_sen.extend(np.where(ordinal_features == tag)[0])
    
    while i<(max_len-1):
        i+=1
        #vector_sen.extend(np.where(ordinal_features == 'None')[0])
        vector_sen.extend([-1])
    return vector_sen
# In[8]
#for onehot encoding
onehot_labels = list(tagdict.keys()) + ['None']

# In[]
'''
def positional_matrix(seq_len=max_len, d=46, n=10000):
    P = np.zeros((seq_len, d))
    for k in range(seq_len):
        for i in np.arange(int(d/2)):
            denominator = np.power(n, 2*i/d)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i+1] = np.cos(k/denominator)
    return P

positional_matrix = positional_matrix()
'''
# In[]


def onehotEncode_titles(titles):
    onehot_matrix = np.empty(shape = (0,24*46))
    
    
    for title in titles:
        onehot_zeros = np.zeros(shape=(max_len, len(onehot_labels)))
        onehot_zeros[:,-1] = 1 
        word_tags = [tag[1] for tag in nltk.pos_tag(nltk.word_tokenize(title))]
        for i, tag in enumerate(word_tags):
            j = onehot_labels.index(tag)
            onehot_zeros[i,j] = 1
            onehot_zeros[i,-1] = 0
      #  onehot_zeros += positional_matrix
        onehot_matrix = np.vstack((onehot_matrix, onehot_zeros.flatten()))
    return onehot_matrix

onehot_matrix = onehotEncode_titles(title_list)
# In[]
#for visualiztion
pca_vis = PCA(n_components=2)
x_vis = pca_vis.fit_transform(onehot_matrix)

plt.scatter(x_vis[:,0], x_vis[:,1])

# In[]
#for dimension reduction
pc = PCA(n_components=0.85)
x_red = pca.fit_transform(onehot_matrix)

# In[]
np.save(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_with_pos_mat", onehot_matrix)
    
    
# In[9]
df_sen_vectors = pd.DataFrame(np.empty(shape=(len(title_list), max_len)))

for j, title in enumerate(title_list):
    df_sen_vectors.iloc[j] = sentence_vector_space(title) 


#save to file
df_sen_vectors.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_ordinal_vector_space_pca.csv")

    
