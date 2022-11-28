# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:21:36 2022

@author: Ravit
"""

# In[0]
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.elbow import elbow
# In[]
def positional_matrix(seq_len, d=1, n=10000):
    P = np.zeros((seq_len, d))
    for k in range(seq_len):
        for i in np.arange(int(d/2)):
            denominator = np.power(n, 2*i/d)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i+1] = np.cos(k/denominator)
    return P

# In[1]
df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\POS_ordinal_vector_space.csv")
df.drop(['Unnamed: 0'], axis=1, inplace=True)

titles_df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv") 
titles_df.drop(['Unnamed: 0'], axis=1, inplace=True)


x = df.to_numpy()
positional = positional_matrix(len(titles_df), len(df.columns))
x += positional


# In[2]
pca = PCA(n_components=2)
x = pca.fit_transform(x)

X, y = x[:,0], x[:,1] 
# In[3]
plt.scatter(X,y)
plt.show()
# In[4]
np.random.seed(0)
km = KMeans()
title_visualizer = KElbowVisualizer(km, k=(2,10), random_state=0)

title_visualizer.fit(x)
title_visualizer.show() 
# In[5]
# create instance of Elbow method using K value from 1 to 10.
kmin, kmax = 1, 10
elbow_instance = elbow(x, kmin, kmax)

# process input data and obtain results of analysis
elbow_instance.process()
amount_clusters = elbow_instance.get_amount()  # most probable amount of clusters
wce = elbow_instance.get_wce()  # total within-cluster errors for each K
# In[6]
# perform cluster analysis using K-Means algorithm
centers = kmeans_plusplus_initializer(x, amount_clusters,
                                      amount_candidates=kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()
kmeans_instance = kmeans(x, centers)
kmeans_instance.process()
# obtain clustering results and visualize them
clusters = kmeans_instance.get_clusters()
centers = kmeans_instance.get_centers()
kmeans_visualizer.show_clusters(x, clusters, centers)

# In[7]
cluster_list = [np.nan]*len(titles_df)

for clu, idx in enumerate(clusters):
    for i in idx:
        cluster_list[i] = clu
        
# In[8]
titles_df['xmeans_cluster'] = cluster_list
titles_df.sort_values(by='cluster_Name', inplace=True)