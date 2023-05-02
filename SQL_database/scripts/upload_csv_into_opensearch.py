# -*- coding: utf-8 -*-
"""
Created on Mon May  1 16:45:24 2023

@author: Ravit
"""

import boto3
from requests_aws4auth import AWS4Auth
import csv

# Define your OpenSearch domain and AWS credentials
region = 'us-east-1'
service = 'es'
aws_access_key_id = 'AKIAQVQUWXGIWI7OWP5D'
aws_secret_access_key = 'Zyc/xP0Gw470vszKqi1ol50VHV4MQpUZWXOKIor4' 
open_search_domain = 'search-etech2-pgyjsqgsjmskwafs4nm24r6jou.eu-central-1.es.amazonaws.com'
'''
# Create a connection to OpenSearch
awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, service)
es = boto3.client('es', endpoint_url=open_search_domain, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Read data from CSV file
filename = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\temp.csv'
with open(filename, mode='r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Bulk upload data to OpenSearch
bulk_data = ''
for record in data:
    index_action = {'index': {'_index': 'row_id', '_type': '_doc'}}
    bulk_data += f"{str(index_action)}\n{str(record)}\n"

response = es.bulk(body=bulk_data, refresh=True)
print(response)
'''

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import csv



# Create a connection to OpenSearch
awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, service)
es = Elasticsearch(
    hosts=[{'host': open_search_domain, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# Read data from CSV file
filename = r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\temp.csv'
with open(filename, mode='r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Bulk upload data to OpenSearch
bulk_data = ''
for record in data:
    index_action = {'index': {'_index': 'row_id', '_type': '_doc'}}
    bulk_data += f"{str(index_action)}\n{str(record)}\n"

response = es.bulk(body=bulk_data, refresh=True)
print(response)