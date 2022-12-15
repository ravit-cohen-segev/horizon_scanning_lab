# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 11:51:24 2022

@author: Ravit
"""
import prince

import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd
import numpy as np
import os

# In[]

folder = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\nltk_features\features"
onehot_path = os.path.join(folder, "onehot_before_dim_red.csv")

onehot_df = pd.read_csv(onehot_path).drop(['Unnamed: 0'], axis=1)

df = pd.read_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\final_article_after_all_filtering_fixed_text_parsing.csv")
title_list = df['titles'].to_list()
link_list = df['link'].to_list()

# In[]
# clean onehot matrix alone
# first remove all vectors with only zeros (They are the reason for Nan values in correlation matrix)
for col in onehot_df.columns:
    if len(onehot_df[col].unique()) == 1:
        onehot_df.drop(col,inplace=True,axis=1)


# In[]
#perform mca on matrix
mca = prince.MCA(random_state=42, n_components=onehot_df.shape[1])
mca = mca.fit(onehot_df)

# In[]
# plot scree plot

ev = mca.eigenvalues_
x_ev = range(1, len(ev)+1) 

plt.scatter(x_ev, ev)
plt.plot(x_ev,ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()



plt.savefig(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\nltk_features\features\fifth_iteration\scree_plot_mca_5th_iter.png")
plt.show()

# In[]

# run mca twice with 50 and 100 components
mca_50 = prince.MCA(random_state=42, n_components=50)
mca_50 = mca_50.fit(onehot_df)

X_50 = mca_50.transform(onehot_df)

# run mca twice with 50 and 100 components
mca_100 = prince.MCA(random_state=42, n_components=100)
mca_100 = mca_100.fit(onehot_df)

X_100 = mca_100.transform(onehot_df)


# In[]
# save reduced datasets 
X_50.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\nltk_features\features\fifth_iteration\onehot_mca_50_components_5th_iter.csv")
X_100.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\reddit_crunch_final_results\bertopic\nltk_features\features\fifth_iteration\onehot_mca_100_components_5th_iter.csv")

 




















