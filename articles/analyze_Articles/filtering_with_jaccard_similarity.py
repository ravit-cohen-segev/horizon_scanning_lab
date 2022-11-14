#!/usr/bin/env python
# coding: utf-8

# In[66]:


import numpy as np
import pandas as pd
import networkx


#  1. load techcrunch and reddit posts titles
# 

# In[67]:


crunch_titles_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\techcrunch_RCS\scrapped_titles\techcrunch_scrapped_article_titles.csv"
reddit_titles_path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\reddit_RCS\first_iteration\final_results\after_cleaning\posts_after_filtering_with_titles.csv"


# In[68]:


crunch_df = pd.read_csv(crunch_titles_path)


# In[69]:


reddit_df = pd.read_csv(reddit_titles_path)


# In[70]:


reddit_df


# In[71]:



reddit_df.columns = ['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'domains', 'posts',
       'upvotes', 'last_updated', 'link', 'title']


# In[72]:


crunch_df


# In[23]:


titles_df = pd.concat([reddit_df[['link', 'title']], crunch_df[['link', 'title']]], axis=0)


# In[27]:


titles_df.drop_duplicates(inplace=True)


# In[58]:


titles_df.dropna(axis=0, inplace=True)


# 2. jaccard similarity

# In[60]:


def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  try:
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  except:
    print('problem')
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)


# In[61]:

all_titles = titles_df['title'].to_list()
jaccard_matrix = np.empty((len(all_titles), len(all_titles)))
jaccard_matrix[:] = np.nan
np.fill_diagonal(jaccard_matrix,1.0)


# In[62]:





# In[ ]:





# In[63]:

sim_pairs = []
all_titles = titles_df['title'].to_list()

for i in range(0, len(titles_df)):
    for  j in range(0, i):
        sim = jaccard_similarity(all_titles[int(i)], all_titles[int(j)])
        
        jaccard_matrix[int(i),int(j)] = sim
        jaccard_matrix[int(j),int(i)] = sim
        if sim>0.7:
            sim_pairs.append([i, j])
            


# In[64]:



jaccard_similarity(all_titles[0], all_titles[0])


# In[65]:


jaccard_matrix
    


# In[ ]:

from networkx.algorithms.components.connected import connected_components


def to_graph(l):
    G = networkx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G
# In[]:
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

G = to_graph(sim_pairs)
out_list = list(connected_components(G))

# In[]

#keep all articles in cluster 0 and item number 25 that talks about using crispr from improving crops
keep_idx = list(out_list[0]) + [25]

new_titles_df = titles_df.iloc[keep_idx]
# In[]
new_titles_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\after_filtering_articles_reddit_and_crunch\filtered_articles.csv")