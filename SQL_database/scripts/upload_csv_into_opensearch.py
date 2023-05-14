# -*- coding: utf-8 -*-
"""
Created on Fri May 12 21:53:13 2023

@author: Ravit
"""

import awswrangler as wr
import pandas as pd
# In[]

region_name = 'eu-central-1'
domain_name = 'search-etechdomain-yk2jvwgoe2fdpowiqunkjyoj3q.us-east-1.es.amazonaws.com'
index_name = 'articles_table'
endpoint_url = f'https://{domain_name}'




# In[]
# TODO - add new records parsed correctly and remove the old ones. Replace data already existing in database

# define chunk size
chunk_size = 1000

my_client = wr.opensearch.connect(host=endpoint_url, username='#####', password='######')

# load CSV in chunks and push to OpenSearch
for i, chunk in enumerate(pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\parse_27Apr23_all_timeseries_datasets_v1.csv', chunksize=chunk_size)):
    # preprocess data
    chunk = chunk[~chunk['row_id'].isna()]
    chunk = chunk[chunk['row_id'].apply(lambda x: isinstance(x, int))]
    chunk = chunk.convert_dtypes()
    chunk['article_date'] = pd.to_datetime(chunk['article_date'])
    chunk['data_extraction_date'] = pd.to_datetime(chunk['data_extraction_date'])
    
    # push chunk to OpenSearch
    wr.opensearch.index_documents(client=my_client, index=index_name, doc_type='_doc', documents=chunk.to_dict(orient='records'))

    
    # print progress
    print(f'Uploaded chunk {i+1}')