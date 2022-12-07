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
import string


# In[1]
#Two ways for making features:
#1. title features

#2. Sentence vector representation - taking into account the order of words 

# In[2]

df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
pos_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_ordinal_vector_space.csv")

title_list = df['titles'].to_list()
link_list = df['link'].to_list()


# In[]
# 1. title features
 
max_len = 24


def num_stopwords(text):
    stop_words = set(stopwords.words('english'))  
    word_tokens = word_tokenize(text)
    stopwords_x = [w for w in word_tokens if w in stop_words]
    return len(stopwords_x)



count_chars = []
count_words = []
count_capital_words = []
#count_sent = []
count_unique_words = []
count_stopwords = []

for title in title_list:
    count_chars.append(len(title))
    count_words.append(len(title.split()))
    count_capital_words.append(sum(map(str.isupper,title.split())))
 #   count_sent.append(len(nltk.sent_tokenize(title)))
    count_unique_words.append(len(set(title.split())))
    count_stopwords.append(num_stopwords(title))

    df  = pd.DataFrame([], columns=['text_length', 'word_count', 'capital_words_count', 'count_unique_words', 'count_stopwords'])
    df['text_length'] = count_chars
    df['word_count'] = count_words
    df['capital_words_count'] = count_capital_words
  #  df['count_sentences'] = count_sent
    df['count_unique_words'] = count_unique_words
    df['count_stopwords'] = count_stopwords
     


# In[]
tagdict = load('help/tagsets/upenn_tagset.pickle')
all_tags = list(tagdict)

all_verb_tags = [(i,w) for i, w in enumerate(all_tags) if 'VB' in w]
verb_index = [w[0] for w in all_verb_tags]

all_noun_tags =  [(i,w) for i, w in enumerate(all_tags) if 'NN' in w]
noun_index = [w[0] for w in all_noun_tags]

#gerund (ing)
verb_vbg = 6

#VBZ and VBP
verb_present = [8, 10]

#create features with combination of words. use sequence of tag indices 
#1. problem description

#Ex: need to do ...
vbp_to_vb = [10,1,36]
#EX: is required ... 
vbz_vbn = [8, 2]

#2. solution
#EX: may help...

md_vb = [35,36]

#EX: for solving ...
#in_nn = [29,11]

#EX: for better ...
#in_jjr = [29,32]

#TODO - use another way to count for in sentence. nltk tags for as preposition at all times abd ignores when it's a conjunction

#3. discoveries/news/innovations
# EX: researcher/s developed a ...
nn_vbd = [11,28]
nns_vbd = [40,28]

# Ex: study demonstrates a...
nn_vbz = [11,8]
nns_vbp = [40,10]

# In[]


#add features related to verbs, number of verbs, number of present tense verbs, number of vbg, number of nouns

all_noun_count = []
all_verb_count = []
all_verb_present = []
all_vbg = []
all_word_num = []

for i, row in pos_df.iterrows():
    row_value_counts = row.value_counts() 
    word_idx = row_value_counts.index
    if -1 in word_idx:
        word_idx = word_idx.drop(-1)
    word_num = np.sum([row_value_counts[j] for j in word_idx])
    all_word_num.append(word_num)
        
    noun_counts = np.sum([row_value_counts[j] for j in noun_index if j in row_value_counts])
    all_noun_count.append(noun_counts)
    
    verb_counts =  np.sum([row_value_counts[j] for j in verb_index if j in row_value_counts]) 
    all_verb_count.append(verb_counts)
    
    v_present  = np.sum([row_value_counts[j] for j in verb_present if j in row_value_counts])
    all_verb_present.append(v_present)
    
    if verb_vbg in row_value_counts.index:
        count_vbg = row_value_counts[verb_vbg]
        all_vbg.append(count_vbg)
    else:
        all_vbg.append(0)

#del word_num, noun_counts, verb_counts, count_verb_present, count_vbg


# In[]
#add features to array

if df == None:
    df = pd.DataFrame([])


df['noun_count'] = np.array(all_noun_count) / np.array(all_word_num)
df['verb_count'] = np.array(all_verb_count) / np.array(all_word_num)
df['verb_present'] = np.array(all_verb_present) / np.array(all_word_num)


df['vbg'] = np.array(all_vbg) / np.array(all_word_num)

eps = 10**(-8)

df['vbg/total_verbs'] = df['vbg'] / (df['verb_count'] + eps)
df['verb_present/total_verbs'] = df['verb_present'] / (df['verb_count'] + eps)

# In[]

def is_tag_sequence_in_senetence(l1, l2):
    str1 = "".join([str(l) for l in l1])
    str2 = "".join([str(l) for l in l2])
    if str1 in str2:
        return 1
    return 0
#problem features
all_vbp_to_vb = [] 
all_vbz_vbn = []


#solution
all_md_vb = []


#discoveries
all_nn_vbd = []
all_nns_vbd = []


all_nn_vbz = []
all_nns_vbp = []


for i, row in pos_df.iterrows():
    row_list = row.astype(int).tolist()
        
    all_vbp_to_vb.append(is_tag_sequence_in_senetence(vbp_to_vb, row_list))
    all_vbz_vbn.append(is_tag_sequence_in_senetence(vbz_vbn, row_list))
    all_md_vb.append(is_tag_sequence_in_senetence(md_vb, row_list))
    all_nn_vbd.append(is_tag_sequence_in_senetence(nn_vbd, row_list))
    all_nns_vbd.append(is_tag_sequence_in_senetence(nns_vbd, row_list))
    all_nn_vbz.append(is_tag_sequence_in_senetence(nn_vbz, row_list))
    all_nns_vbp.append(is_tag_sequence_in_senetence(nns_vbp, row_list))
    

df['vbp_to_vb'] = all_vbp_to_vb
df['vbz_vbn'] = all_vbz_vbn
df['md_vb'] = all_md_vb
df['nn_vbd'] = all_nn_vbd
df['nns_vbd'] = all_nns_vbd
df['nn_vbz'] = all_nn_vbz
df['nns_vbp'] = all_nns_vbp



all_fors = []
for title in title_list:
    if 'for' in title:
        all_fors.append(1)
    else:
        all_fors.append(0)

df['for'] = all_fors

df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features\sentence_stat_features.csv')

# In[8]
#2
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
pca = PCA(n_components=0.5)
x_red = pca.fit_transform(onehot_matrix)
# In[]
# plot scree plot
PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_)
plt.title('Scree plot')
plt.xlabel('Principal component')
plt.xticks(ticks = PC_values)
plt.ylabel('Variance explained')
plt.show()

#knee is at point 4

# In[]
#save the matrix that was reduced to n components 
pca = PCA(n_components=4)
x_ = pca.fit_transform(onehot_matrix)


np.save(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\features\POS_after_pca", x_)
    
    
# In[9]

pc_columns = ['pc_1', 'pc_2', 'pc_3', 'pc_4']
df[pc_columns] = pd.DataFrame(x_) 

# In[]

#save to file
df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features\title_stats_pc_components.csv")

    
