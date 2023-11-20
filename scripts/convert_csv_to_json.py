# -*- coding: utf-8 -*-
"""
Created on Mon May  8 12:11:20 2023

@author: Ravit
"""

import pandas as pd
import datetime

csvFilePath = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.csv'
jsonFilePath = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.json'


# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csvFilePath)
df = df[~df['row_id'].isna()]
df = df[df['row_id'].apply(lambda x: isinstance(x, int))]
df = df.convert_dtypes()

# Convert the DataFrame to JSON
json_df = df.to_json()

# Write the JSON to a file
with open(jsonFilePath, 'w') as f:
    f.write(json_df)