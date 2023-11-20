# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:03:13 2023

@author: Ravit
"""

import json
import os
import pandas as pd

# In[]
path = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\sample_json_core.json'

            
# In[]

def json_to_df(data):
    for key in data.keys():   
        data[key] = [data[key]]

    df = pd.DataFrame(data)
    return df

# In[]
dfs = []

with open(path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            json_data = json.loads(line)
            # Process the JSON object
            dfs.append(json_to_df(json_data))
            
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            
# In[]
all_dfs = pd.concat(dfs)