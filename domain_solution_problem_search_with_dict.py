# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 10:33:34 2023

@author: Ravit
"""

import pandas as pd
import json

import nltk
from nltk.tokenize import word_tokenize 

# In[]
f = open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\dict\problem_solution_dict.txt')
d = json.loads(f.read())

df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\scrappers\techcrunch_RCS\scrapped_titles\techcrunch_scrapped_ag_titles.csv')

# In[]
solution_words = d['solutions']
problem_words = d['problems']

# In[]
df_solution = pd.DataFrame([], columns=df.columns)
df_problem = pd.DataFrame([], columns=df.columns)

solution = ['0']*len(df)
problem =  ['0']*len(df)


for i, row in df.iterrows():
    title_words = word_tokenize(df['title'][0].lower())
    
    row.columns = df.columns
    for w in title_words:
        if w in solution_words:
            df_solution = pd.concat([df_solution, row.to_frame().T])
            solution[i] = '1'
            
            
        if w in problem_words:
            df_problem = pd.concat([df_problem, row.to_frame().T])
            problem[i] = '1'
            


