# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 16:05:26 2023

@author: Ravit
"""

from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib


g = rdflib.Graph()
g.parse(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\dict\nalt_full_2022-07-28_ttl\nalt_full.ttl', format = 'ttl')
# In[]
df = to_dataframe(g)
df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\agriculture_data\dict\nalt_full_2022.csv', index = True)