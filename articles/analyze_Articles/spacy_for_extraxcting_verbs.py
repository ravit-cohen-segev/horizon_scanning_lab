# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import unicode_literals, annotations
import pandas as pd

import spacy
from spacy.util import filter_spans
from spacy.matcher import Matcher
import numpy as np

# In[0]
path = r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\final_article_after_all_filtering.csv"
df = pd.read_csv(path)
# In[1]
#save titles to list
titles = df['titles'].to_list()

# In[3]
nlp = spacy.load('en_core_web_sm') 

pattern = [[{'POS': 'VERB', 'OP': '?'}],
           [{'POS': 'VERB', 'OP': '+'}]]

# instantiate a Matcher instance
matcher = Matcher(nlp.vocab)
matcher.add("Verb phrase", pattern)

doc = nlp(titles[0]) 
# call the matcher to find matches 
matches = matcher(doc)
spans = [doc[start:end] for _, start, end in matches]

print(filter_spans(spans))   
# In[3]

def pos_from_docs_with_spacy(texts, pattern):

    # instantiate a Matcher instance
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", pattern)
    
    verb_spans = {}
    
    for i,text in enumerate(texts):
        doc = nlp(text) 
        # call the matcher to find matches 
        matches = matcher(doc)
        spans = [doc[start:end] for _, start, end in matches]
        verb_spans[str(i)] = [str(s) for s in spans]
    return verb_spans


# In[4]

def create_one_strings(d):
    str_list = []
    for key, val_list in d.items():
        str_words =  []
        for w in val_list:
            str_words += w.split()
        str_list.append(" ".join(list(set(str_words))))
    return str_list
    

# In[5]

verb_pattern = [[{'POS': 'VERB', 'OP': '?'}],
               [{'POS': 'VERB', 'OP': '+'}]]

noun_pattern = [[{'POS': 'NOUN'}]]
    

verb_d = pos_from_docs_with_spacy(titles, verb_pattern)

noun_d = pos_from_docs_with_spacy(titles, noun_pattern)

out_df = pd.DataFrame(np.empty(shape=(len(titles), 4)), columns=['link', 'title', 'spacy_verbs', 'spacy_nouns'])
out_df['title'] = titles
out_df['link'] = df['link']
out_df['spacy_verbs'] = create_one_strings(verb_d)
out_df['spacy_nouns'] = create_one_strings(noun_d)

out_df.to_csv(r"C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\articles\analyze_Articles\final_results\bertopic\extracted_verbs_nouns_before_bertopic.csv")
