# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 11:51:24 2022

@author: Ravit
"""

from sklearn.decomposition import PCA, FactorAnalysis
from factor_analyzer import FactorAnalyzer

import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd
import numpy as np
import os

# In[]

folder = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features"
det_path = os.path.join(folder, r"fourth_iteration\deterministic_features_4th_iteration.xlsx")
onehot_path = os.path.join(folder, "onehot_before_dim_red.csv")

dm_df = pd.read_excel(det_path).drop(['Unnamed: 0'], axis=1)
onehot_df = pd.read_csv(onehot_path).drop(['Unnamed: 0'], axis=1)

df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
title_list = df['titles'].to_list()
link_list = df['link'].to_list()

# In[]
#concat dfs
conc_df = pd.concat([dm_df,  onehot_df], axis=1)
conc_df.columns = list(dm_df.columns) + list(onehot_df.columns)
# In[]
# 1. Perfom PCA

#for visualiztion
pca_vis = PCA(n_components=2)
x_vis = pca_vis.fit_transform(conc_df)

plt.scatter(x_vis[:,0], x_vis[:,1])

# In[]
#for dimension reduction
pca = PCA(n_components=0.9)
x_red = pca.fit_transform(conc_df)
# In[]
# plot scree plot
PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_)
plt.title('Scree plot')
plt.xlabel('Principal component')
plt.xticks(ticks = PC_values)
plt.ylabel('Variance explained')
plt.show()
# save screeplot graph (manually), and x_red

pca_df = pd.DataFrame(x_red)
pca_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features\fourth_iteration\PCA_4th_iteration_all_features.csv")

    

# In[10]
# 2. perform factor analysis
# first remove all vectors with only zeros (They are the reason for Nan values in correlation matrix)
for col in conc_df.columns:
    if len(conc_df[col].unique()) == 1:
        conc_df.drop(col,inplace=True,axis=1)
        
# add noise to data to avoid Singular Matrix error
dfDirty = conc_df+0.00001*np.random.rand(conc_df.shape[0], conc_df.shape[1])

# In[]
fa = FactorAnalyzer(21)

X_transformed = fa.fit_transform(dfDirty)
# In[] 
# plot screeplot for factor 
ev, v = fa.get_eigenvalues()

plt.scatter(range(1, dfDirty.shape[1]+1),ev)
plt.plot(range(1,dfDirty.shape[1]+1),ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.show()


# In[]
# save screeplot graph (manually), and x_red

fa_df = pd.DataFrame(X_transformed)
pca_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\nltk_features\features\fourth_iteration\FA_4th_iteration_all_features.csv")