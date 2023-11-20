# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:59:53 2023

@author: Ravit
"""

import boto3
import pandas as pd
from pyathena import connect

# AWS credentials
aws_access_key_id = ''
aws_secret_access_key = '' 

#aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_region = 'eu-central-1'

# S3 bucket information
s3_bucket = 'technologydb'
s3_prefix = 'csv_data/'

# Athena information
database_name = 'ET_tables'
table_name = 'articles'

#Connect to Athena
conn = connect(s3_staging_dir='s3://{}/athena'.format(s3_bucket),
               region_name=aws_region,
               aws_access_key_id=aws_access_key_id,
               aws_secret_access_key=aws_secret_access_key)
  


# Define the SQL query to create the Athena table
create_table_query = '''
    CREATE EXTERNAL TABLE IF NOT EXISTS {}.{} (
        row_id INT, 
        article_id INT,
        journal_id INT, 
        article_source STRING, 
        source_link STRING,
        article_title STRING,
        article_link STRING, 
        article_date DATE,
        article_text STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION 's3://{}/{}'
    TBLPROPERTIES ("skip.header.line.count"="1")
'''.format(database_name, table_name, s3_bucket, s3_prefix)

# Execute the SQL query to create the Athena table
with conn.cursor() as cursor:
    cursor.execute(create_table_query)

# Read the CSV data into a Pandas DataFrame
csv_data = pd.read_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\feature_scripts\docs\timeline_datasets\we_forum\17Apr23_weforum_parsehub_all_articles_2014_to_2023.csv')

# make sure that csv table has the right order of columns
assert set(csv_data.columns) == set(['row_id', 'article_id', 'journal_id', 'article_source', 'source_link', 'article_title', 'article_link', 'article_date', 'article_text'])


# Write the CSV data to S3
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)
s3_client.put_object(Body=csv_data.to_csv(index=False),
                     Bucket=s3_bucket,
                     Key=s3_prefix + 'we_forum.csv')

# In[]
# Execute a query to add the CSV data to the Athena table
with conn.cursor() as cursor:
    cursor.execute('MSCK REPAIR TABLE {}.{}'.format(database_name, table_name))
    cursor.execute('INSERT INTO TABLE {}.{} SELECT * FROM {}.{}'.format(database_name, table_name, database_name, table_name))
    cursor.execute('SELECT COUNT(*) FROM {}.{}'.format(database_name, table_name))
    result = cursor.fetchone()
    print('Added {} rows to table {}'.format(result[0], table_name))