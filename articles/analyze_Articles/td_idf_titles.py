# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 09:20:15 2022

@author: Ravit
"""

# In[0]
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import en_core_web_sm
import spacy
import os
import string
import re
import nltk
from nltk.tokenize import TweetTokenizer
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.decomposition import TruncatedSVD
import networkx
from networkx.algorithms.components.connected import connected_components
from sklearn.metrics.pairwise import cosine_similarity
import hdbscan
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from cycler import cycler

# In[1]
nlp = en_core_web_sm.load()

def spacy_tokenizer(document):
    tokens = nlp(document)
    tokens = [token.lemma_ for token in tokens if (
        token.is_stop == False and \
        token.is_punct == False and \
        token.lemma_.strip()!= '')]
    return tokens

def clean_text(text):
    # remove numbers
    text_nonum = re.sub(r'\d+', '', text)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation ])
    text_split = text_nopunct.split()
    #keep words that have more than 1 letter, for instance 1M$->m
    text = " ".join([w for w in text_split if len(w)>1])
    
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    text_no_doublespace = re.sub('\s+', ' ', text).strip()
    encoded_text = text_no_doublespace.encode("ascii", "ignore")
    return encoded_text.decode()

def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  try:
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  except:
    print('problem')
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

def to_edges(l):
    """ 
        treat `l` as a Graph and returns it's edges 
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current 


def to_graph(l):
    G = networkx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G




# In[2]
#read questions from df
path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\article_bertopic_titles_textrank_final.csv"

titles_df = pd.read_csv(path)
titles_df = titles_df[['link', 'titles', 'abstract']]
titles_df.drop_duplicates(subset='titles', inplace=True)
titles_df.dropna(subset='titles', inplace=True)
titles = titles_df['titles'].to_list()


# In[3] 
#remove digits and punctuations from title sentences

for i, title in enumerate(titles):
    titles[i] = clean_text(titles[i])
    
#titles = len(set(titles))

# In[4]
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english', tokenizer=spacy_tokenizer)
X = vectorizer.fit_transform(titles)
features = vectorizer.get_feature_names_out()
transformed_documents_as_array = X.toarray()


# In[8]
#use jaccard similarity to identfy titles that may indicate breakthroughs or new techs

jaccard_matrix = np.empty((len(titles), len(titles)))
jaccard_matrix[:] = np.nan
np.fill_diagonal(jaccard_matrix,1.0)

sim_pairs = []

for i in range(0, len(titles)):
    for  j in range(0, i):
        sim = jaccard_similarity(titles[int(i)], titles[int(j)])
        
        jaccard_matrix[int(i),int(j)] = sim
        jaccard_matrix[int(j),int(i)] = sim
        if sim>0.899:
            sim_pairs.append([i, j])
    
G = to_graph(sim_pairs)
out_list = list(connected_components(G))


# In[10]
#add jaccard sim tags to df

cluster_list = [np.nan]*len(titles)
for i, values in enumerate(out_list):
    for val in values:
        cluster_list[val] = i
        
titles_df['title_sim_tag'] = cluster_list
titles_df.sort_values(by='title_sim_tag', inplace=True)

#remove all titles that don't beling to a group
not_null_tags_index = ~titles_df['title_sim_tag'].isna()
new_titles_df = titles_df[not_null_tags_index]
new_titles = new_titles_df['titles'].to_list()


# In[13]
#Do the same for abstracts
abstracts = new_titles_df['abstract'].to_list()

abs_vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english', tokenizer=spacy_tokenizer)
X_abs = abs_vectorizer.fit_transform(abstracts)
abs_features = abs_vectorizer.get_feature_names_out()
transformed_abstracts_as_array = X_abs.toarray()

# In[]
#use jaccard similarity to identfy titles that may indicate breakthroughs or new techs

jaccard_abs_matrix = np.empty((len(abstracts), len(abstracts)))
jaccard_abs_matrix[:] = np.nan
np.fill_diagonal(jaccard_abs_matrix,1.0)

sim_pairs = []

for i in range(0, len(abstracts)):
    for  j in range(0, i):
        sim = jaccard_similarity(abstracts[int(i)], abstracts[int(j)])
        
        jaccard_abs_matrix[int(i),int(j)] = sim
        jaccard_abs_matrix[int(j),int(i)] = sim
        if sim>0.8:
            sim_pairs.append([i, j])
    
G = to_graph(sim_pairs)
out_list = list(connected_components(G))

# In[]
abs_cluster_list = [np.nan]*len(abstracts)
for i, values in enumerate(out_list):
    for val in values:
        abs_cluster_list[val] = i
        
new_titles_df['abs_sim_tag'] = abs_cluster_list
new_titles_df.sort_values(by='abs_sim_tag', inplace=True)
# In[]

new_not_null_tags_index = ~new_titles_df['abs_sim_tag'].isna()
new_titles_df = new_titles_df[new_not_null_tags_index]

# In[]
new_titles_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\jaccard_filtered\reddit_crunch_filtered.csv")