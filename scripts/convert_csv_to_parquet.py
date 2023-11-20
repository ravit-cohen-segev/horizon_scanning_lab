# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:38:54 2023

@author: Ravit
"""

import pandas as pd

# read the CSV file using pandas
df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.csv')



df.to_parquet(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.parquet', compression='snappy')

# In[]
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.csv')
df = df[~df['row_id'].isna()]
df = df[df['row_id'].apply(lambda x: isinstance(x, int))]

# In[]
# Convert the pandas DataFrame to a pyarrow Table
table = pa.Table.from_pandas(df)

# Write the pyarrow Table to a Parquet file using the ParquetWriter
pq.write_table(table, r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.parquet')
