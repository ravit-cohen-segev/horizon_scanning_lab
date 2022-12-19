# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:04:14 2022

@author: Ravit
"""

import json
import pandas as pd 
from bs4 import BeautifulSoup


# In[]
def parse_categories(categories):
    for i, sub in enumerate(categories):
        sub = sub.split('(')
        sub[1] = sub[1].replace(')','')
        categories[i] = sub
    return categories


# In[]
with open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\arxiv_RCS\scripts\category_taxonomy') as f:
    text = f.read().replace('\n', '')

soup = BeautifulSoup(text)


#get all accordion-head categories
accordion_heads = soup.find_all("h2", {"class": "accordion-head"})

head_categories = [head.text for head in accordion_heads]

category_dict = {}

for cat in head_categories:
    if cat == 'Computer Science':
        initials = 'cs'
    if cat == 'Economics':
        initials = 'econ'
    if cat == 'Electrical Engineering and Systems Science':
        initials = 'eess'
    if cat == 'Mathematics':
        initials = 'math'
    if cat == 'Mathematics':
        initials = 'math'
    if cat == 'Quantitative Biology':
        initials = 'q-bio'
    if cat == 'Quantitative Finance':
        initials = 'q-fin'   
    if cat == 'Statistics':
        initials = 'stat'        
      
    category_dict[cat] = initials
    
physics_sub_cats = {}

phys_categories = soup.find_all('h3')[1:]
phys_categories = parse_categories([phy.text for phy in phys_categories])

for phy in phys_categories:
    physics_sub_cats[phy[0]] = phy[1]
    
category_dict['Physis'] = physics_sub_cats

# In[]


with open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\Scrapers\arxiv_RCS\scripts\docs\arxiv_categories.json', 'w') as f:
    json.dump(category_dict, f)



























category_tree = {}

