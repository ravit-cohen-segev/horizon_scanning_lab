# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 15:28:07 2022

@author: Ravit
"""

# In[0]
import pandas as pd 
import numpy as np
import itertools
from nltk.data import load

from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer, cluster_visualizer_multidim

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
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
 
# In[1]
np.random.seed(42)

pos_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_ordinal_vector_space.csv")
text_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")

pos_df.drop(['Unnamed: 0'], axis=1, inplace=True)

df = None

# In[9]

#onehot_matrix = np.load(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_with_pos_mat.npy")
# In[10]
#remove features with low variance
#onehot_df = pd.DataFrame(onehot_matrix)
#variance = onehot_df.var()

#variable = [ ]

#for i in range(0,len(variance)):
 #   if variance[i]>=0.25: #setting the threshold as 1%
  #      variable.append(i)

#onehot_df = onehot_df[variable] 

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


#find all titles with 'for' in them
title_list = text_df['titles']

all_fors = []
for title in title_list:
    if 'for' in title:
        all_fors.append(1)
    else:
        all_fors.append(0)

df['for'] = all_fors

# In[]

def divide_chunks(li, n):
    # looping till length l
    for i in range(0, len(li), n):
        yield li[i:i + n]

x = df.to_numpy()
l = np.arange(x.shape[1]).tolist()

pair_filters = list(itertools.product(l,l))
pair_filters = [a for a in pair_filters if a[0]!=a[1]]
pair_filters = list(divide_chunks(pair_filters, n=1))
        
x = x.tolist()

# In[11]
# Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
# start analysis.
amount_initial_centers = 2
initial_centers = kmeans_plusplus_initializer(x, amount_initial_centers).initialize()

# Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
# number of clusters that can be allocated is 20.
xmeans_instance = xmeans(x, initial_centers, 6)
xmeans_instance.process()
 
# Extract clustering results: clusters and their centers
clusters = xmeans_instance.get_clusters()
centers = xmeans_instance.get_centers()

#visualize the clusters
visualizer = cluster_visualizer_multidim()
visualizer.append_clusters(clusters, x)

visualizer.show(max_row_size=10)

'''
for pair_filter in pair_filters:
    visualizer.show(pair_filter=pair_filter, max_row_size=2)
'''
# Print total sum of metric errors
print("Total WCE:", xmeans_instance.get_total_wce())
# In[12]
#reduce dimensions with pca

pca = PCA(n_components=2)
x_red = pca.fit_transform(x)

plt.scatter(x=x_red[:,0], y=x_red[:,1])
# In[]
# plot interactive graphs with plotly
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *


n_size = [20]*len(x_red)
n_text = [str(i) for i in range(len(x_red))]


trace0 = Scatter(
    x=x_red[:,0],
    y=x_red[:,1],
    text= n_text,
    mode='markers',
    marker=dict(
        size=n_size,
    )
)
data = [trace0]
layout = Layout(
    showlegend=False,
    height=600,
    width=600,
)

fig = dict( data=data, layout=layout )

plot(fig)  


# In[13]

out_pos_df = text_df[['link', 'titles', 'abstract']]
cluster_list = [np.nan]*len(out_pos_df)

for c_id in range(len(clusters)):
    for i in clusters[c_id]:
        cluster_list[i] = c_id
# In[]

out_pos_df['xmeans_labels'] = cluster_list
out_pos_df = out_pos_df.sort_values(by='xmeans_labels')

text_df['xmeans_labels'] = cluster_list
text_df = text_df.sort_values(by='xmeans_labels')
# In[]
text_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\xmeans_clusters_second_attempt.csv")
