# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:45:58 2023

@author: Ravit
"""

from nltk.corpus import wordnet
import json

# In[]
def get_syn(word):
    syns = wordnet.synsets(word)
    
    synonyms = []

    for syn in syns:
        for l in syn.lemmas():
            synonyms.append(l.name())
    return [s.lower().replace('_',' ') for s in synonyms]

# In[]


syns = get_syn('agriculture')
syns_2 = get_syn("agricultural")

syns.extend(syns_2)
syns = list(set(syns))


li = ['farming', 'stock farming', 'agricultural', 'cultivation of the land',  'agricultural surplus', 'farmed', 'agricultura', 'agricultural methods', 'agricultural practices', 'agricultural industry', 'agricultural supply store', 
      'agricultural systems', 'farm sector', 'agricultural produce', 'farm safety', 'agricultural production']

ag_dict = {'ag_terms':syns + li}

json_file = json.dumps(ag_dict)
with open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\agriculture_terms.json', 'w') as f:
    f.write(json_file)