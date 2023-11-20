# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 13:23:48 2023

@author: Ravit
"""

import boto3

# Set up the Athena client
athena_client = boto3.client('athena')

# Set up the S3 resource
s3_resource = boto3.resource('s3')

# Set the S3 path to the CSV file
s3_path = 's3://technologydb/my_table.csv'

# Set the Athena database and table names
database_name = 'ET_tables'
table_name = 'my_athena_table'

# Create the Athena table if it doesn't already exist
create_table_query = f"CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (col1 string, col2 string, col3 int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' LOCATION '{s3_path}'"
athena_client.start_query_execution(QueryString=create_table_query)

# Run the COPY command to load data into the Athena table
copy_query = f"COPY {database_name}.{table_name} FROM '{s3_path}' WITH (FORMAT 'CSV', DELIMITER ',', IGNOREHEADER 1)"
athena_client.start_query_execution(QueryString=copy_query)

# Wait for the query to complete
query_execution_id = athena_client.start_query_execution(QueryString=copy_query)['QueryExecutionId']
query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']
while query_status == 'RUNNING':
    query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']

# Print the query results
result_query = f"SELECT * FROM {database_name}.{table_name}"
result = athena_client.start_query_execution(QueryString=result_query)['QueryExecutionId']
result_location = athena_client.get_query_execution(QueryExecutionId=result)['QueryExecution']['ResultConfiguration']['OutputLocation']
result_file = s3_resource.Object(result_location.replace('s3://', '').split('/', 1)[0], result_location.replace('s3://', '').split('/', 1)[1]).get()['Body'].read().decode('utf-8')
print(result_file)
