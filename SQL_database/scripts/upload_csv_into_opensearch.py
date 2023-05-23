# -*- coding: utf-8 -*-
"""
Created on Fri May 12 21:53:13 2023

@author: Ravit
"""

import awswrangler as wr
import pandas as pd
import re
# In[]

region_name = 'eu-central-1'

domain_name = 'search-etechdbsearch-6hrir27ks2ye5xnfwcnvmlppbe.eu-central-1.es.amazonaws.com'

index_name = 'articles_table'
endpoint_url = f'https://{domain_name}'




# In[]
# TODO - add new records parsed correctly and remove the old ones. Replace data already existing in database

# define chunk size
chunk_size = 1000

my_client = wr.opensearch.connect(host=endpoint_url, username='###', password='###')

# load CSV in chunks and push to OpenSearch
for i, chunk in enumerate(pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\parsed_files_ready_for_db\27Apr23_all_timeseries_datasets_v3.csv', chunksize=chunk_size, 
                                      dtype={'row_id': 'Int64', 'journal_id': 'Int64', 'article_source':'str', 'article_journal':'str', 'article_doi':'str', 'article_category':'str', 'article_title':'str', 'article_abstract':'str', 
                                             'article_text':'str', 'article_notes':'str', 'article_authors':'str', 'article_link':'str', 'source_link':'str', 'article_id':'str'}, parse_dates=['article_date','data_extraction_date','article_date_by_month'])):
    chunk = chunk.fillna('')
    # push chunk to OpenSearch
    wr.opensearch.index_documents(client=my_client, index=index_name, doc_type='_doc', documents=chunk.to_dict(orient='records'), refresh=True)

    
    # print progress
    print(f'Uploaded chunk {i+1}')