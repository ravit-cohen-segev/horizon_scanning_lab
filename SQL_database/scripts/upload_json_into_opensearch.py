# -*- coding: utf-8 -*-
"""
Created on Mon May  1 16:45:24 2023

@author: Ravit
"""
import boto3
import json
from elasticsearch import Elasticsearch


# Define your OpenSearch domain and AWS credentials
region_name = 'eu-central-1'
domain_name = 'search-etech-dtnrcl2if6rlcml7hdtz4zrlk4.us-east-1.es.amazonaws.com'
endpoint_url = f'https://{domain_name}'
index_name = 'row_id'
json_file = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\temp.json'


opensearch_client = boto3.client('es', region_name=region_name)

# Create an Elasticsearch client with the endpoint URL
es = Elasticsearch(endpoint_url,
                   http_auth=('ravit', 'Horizon1%'))

# Upload the JSON file to OpenSearch using the Elasticsearch client
with open(json_file, 'r') as f:
    json_data = json.load(f)

bulk_data = []
for data in json_data:
    bulk_data.append({
        "index": {
            "_index": index_name,
        }
    })
    bulk_data.append(data)

response = es.bulk(index=index_name, body=bulk_data, refresh=True)

print(f"Uploaded {len(json_data)} documents to OpenSearch index {index_name}")
