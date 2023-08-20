#!/usr/bin/env python
# coding: utf-8

# In[60]:


import re
import os
import glob
import json 
import numpy as np
import pandas as pd
import boto3
import gzip
import io
import awswrangler as wr
import datetime
import pytz

# In[]

def standardize_timestamps(ts):
    # Convert everything to Timestamp first
    ts = pd.Timestamp(ts)

    # If the time is naive, localize it to the initial timezone (could be your local timezone)
    if ts.tzinfo is None or ts.tzinfo.utcoffset(ts) is None:
        ts = ts.tz_localize('UTC')  # Use 'UTC' or any other timezone you think the naive times might be in

    # Convert the time to UTC
    ts = ts.tz_convert('UTC')

    return ts

def check_date_string(s):
    try:
        pd.Timestamp(s)
        return True
    except:
        return False



def convert_jsons_to_big_frame(data_list):
    all_dfs = pd.DataFrame()
    
    for data in data_list:
        
        enrichments = data.pop('enrichments')
        data['references'] = enrichments['references']
        data['citationCount'] = enrichments['citationCount'] 
        data['documentType_type'] = enrichments['documentType']['type']
        data['documentType_confidence'] = enrichments['documentType']['confidence']
        
        for k,v in data.items():
            data[k] = str(v)
        
        data = pd.DataFrame(data, index=[0])
        # Convert to numeric type
        data['citationCount'] = pd.to_numeric(data['citationCount'].replace('None','0'))
        data['documentType_confidence'] = pd.to_numeric(data['documentType_confidence'].replace('None','0'))
        data['coreId'] = pd.to_numeric(data['coreId'])
        data['magId'] = pd.to_numeric(data['magId'].replace('None','0'))
        

        # convert to datetime - year
        data['year'] = data['year'].replace('None','1777')
        
        #check for years that are in the future/ not true
        current_year = datetime.datetime.now().year
        current_date = datetime.date.today()
        past_year = 1777 
        
        # Replace 'None' or None with a valid date or np.nan
       # data['datePublished'].replace({'None': '1777-01-01', None: '1777-01-01'}, inplace=True)
        
        # Filter out valid date strings
        invalid_dates = data[~data['datePublished'].apply(check_date_string)]['datePublished']

        # Replace problematic dates with a default date (e.g., '1777-01-01')
        data.loc[~data['datePublished'].apply(check_date_string), 'datePublished'] = '1777-01-01'

        # Convert date strings to standardized datetime objects
        data['datePublished'] = data['datePublished'].apply(standardize_timestamps)

        threshold_date = pd.Timestamp('1777-01-01').tz_localize('UTC')
        data.loc[data['datePublished'] < threshold_date, 'datePublished'] = threshold_date

        # Convert to "year-month-day" format
        data['datePublished'] = data['datePublished'].dt.strftime('%Y-%m-%d')

      
        data.loc[data['year'].astype(int) > current_year, 'year'] = '1777'
        

        data.loc[data['year'].astype(int) < past_year, 'year'] = '1777'
        
        data['year'] = pd.to_datetime(data['year'])
        
        def remove_timezone(string):
          pattern = r'\+\d\d:\d\d'
          result = re.sub(pattern, '', string)
          if result.isdigit():
              return result
          else:
              return ''
      
      
        data['datePublished'] = data['datePublished'].str.replace('issued','',regex=True).str.replace('[[]]','',regex=True).str.replace('[[]]','',regex=True)
       
       
        try:
            data['datePublished'] = pd.to_datetime(data['datePublished'].apply(lambda x: remove_timezone(str(x)))).fillna(1777).copy()
        except:
            print('there is a date issue')
        
        data = data.convert_dtypes()
       
        
        #concat all 
        all_dfs = pd.concat([all_dfs, pd.DataFrame(data)])

    return all_dfs
        


# In[61]:
s3 = boto3.client('s3')

# The bucket and the file name
bucket = 'technologydb'
folder = 'jsonl'

region_name = 'eu-central-1'

domain_name = 'search-etechdbsearch-6hrir27ks2ye5xnfwcnvmlppbe.eu-central-1.es.amazonaws.com'

index_name = 'core_db'
endpoint_url = f'https://{domain_name}'

my_client = wr.opensearch.connect(host=endpoint_url, username='horizondb', password='Et123456@')

# In[]
# List objects in the folder
response = s3.list_objects(Bucket=bucket, Prefix=folder)
failed_uploads = []


# Iterate over the objects
for obj in response['Contents']:
    key = obj['Key']
    
    # Skip the folder itself
    if key == folder:
        continue
    # Get the .gz file from S3
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    
    # Wrap the bytes in a file-like object using io, then decompress it using gzip
    gzipfile = gzip.GzipFile(fileobj=io.BytesIO(file_obj['Body'].read()))

    # Read the decompressed bytes and decode it into text
    text = gzipfile.read().decode('utf-8')
    #separate jsons with spaces
    text = text.replace('}{', '}\n{')
    # Split the text into lines and parse each line as JSON

    try:
        json_data = [json.loads(line) for line in text.splitlines()]
        parsed_json = convert_jsons_to_big_frame(json_data)      
        
        # upload parsed file to opensearch
        wr.opensearch.index_documents(client=my_client, index=index_name, doc_type='_doc', documents=parsed_json.to_dict(orient='records'), refresh=True)
        print(f'successfully uploaded {obj}')
    except:
        failed_uploads.append(obj)
# In[]
with open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\8Aug23_prob_core_json_files.text', 'wt') as f:
    f.write(str(failed_uploads))

        
