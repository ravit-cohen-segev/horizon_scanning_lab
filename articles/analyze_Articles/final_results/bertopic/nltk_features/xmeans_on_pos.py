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
from sklearn.preprocessing import MinMaxScaler

from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *

import matplotlib.pyplot as plt
import seaborn as sns

# In[1]
text_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
features_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features\title_stats_pc_components.csv")


# In[]
np.random.seed(42)

def divide_chunks(li, n):
    # looping till length l
    for i in range(0, len(li), n):
        yield li[i:i + n]

x = features_df.to_numpy()

scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x)

# In[]
l = np.arange(x_scaled.shape[1]).tolist()

pair_filters = list(itertools.product(l,l))
pair_filters = [a for a in pair_filters if a[0]!=a[1]]
pair_filters = list(divide_chunks(pair_filters, n=1))

# In[]    
x_ = x_scaled.tolist()

# In[11]
# Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
# start analysis.



amount_initial_centers = 2
initial_centers = kmeans_plusplus_initializer(x_, amount_initial_centers, random_state=42).initialize()

# Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
# number of clusters that can be allocated is 20.
xmeans_instance = xmeans(x_, initial_centers, 6, tolerance=0.00085)
xmeans_instance.process()
 
# Extract clustering results: clusters and their centers
clusters = xmeans_instance.get_clusters()
centers = xmeans_instance.get_centers()

'''
#visualize the clusters
visualizer = cluster_visualizer_multidim()
visualizer.append_clusters(clusters, x_comb)

visualizer.show(max_row_size=10)'''

'''
for pair_filter in pair_filters:
    visualizer.show(pair_filter=pair_filter, max_row_size=2)
'''
# Print total sum of metric errors
print("Total WCE:", xmeans_instance.get_total_wce())
# In[12]
#reduce dimensions with pca

pca = PCA(n_components=2)
x_red = pca.fit_transform(x_)


# In[13]

out_pos_df = text_df[['link', 'titles', 'abstract']]
cluster_list = [np.nan]*len(out_pos_df)

for c_id in range(len(clusters)):
    for i in clusters[c_id]:
        cluster_list[i] = c_id


# In[]
# plot interactive graphs with plotly

def plot_xmeans(x, y, cluster_list):
    n_size = [20]*len(x_red)
    n_text = list(zip([str(i) for i in range(len(x_red))], cluster_list))


    trace0 = Scatter(
    x=x,
    y=y,
    text= n_text,
    mode='markers',
    marker=dict(
        size=n_size, color = cluster_list
    )
    )
    data = [trace0]
    layout = Layout(
        showlegend=False,
        height=2000,
        width=2000,
        )

    fig = dict( data=data, layout=layout )

    plot(fig)


plot_xmeans(x_red[:,0],x_red[:,1], cluster_list)


# In[]


text_df['xmeans_labels'] = cluster_list
text_df = text_df.sort_values(by='xmeans_labels')
# In[]
text_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\xmeans_clusters_third_attempt.csv")
# In[]
# TODO -> complete this

#plot distribution of topics per cluster
#text_df[['bertopic_cluster_id', 'xmeans_labels']].hist(by=text_df['bertopic_cluster_id'])
