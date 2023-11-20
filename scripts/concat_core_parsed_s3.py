# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 09:13:03 2023

@author: Ravit
"""

import pandas as pd
import numpy as np
import pyspark.pandas as ps
import boto3
from pyspark.sql import SparkSession
import io
from functools import reduce
from tqdm import tqdm

# Initial setup
s3_client = boto3.client('s3')
bucket_name = 'technologydb'
prefix = 'core_jsonl_parsed_/jsonl/'  # Make sure it ends with a '/'

# Create a Spark session
spark = SparkSession.builder.appName("ParquetExample").getOrCreate()

def list_parquet_files(bucket, prefix):
    """
    List all parquet files in a specified S3 bucket at a specified prefix
    """
    files = []
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    for page in pages:
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                files.append(obj['Key'])
    
    return files

def read_parquet_from_s3(bucket, key):
    """
    Read a parquet file from S3 and return it as a polars DataFrame
    """
    response = s3_client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read()
    df = spark.read.parquet(io.BytesIO(data))
    return  df

# Walking through the S3 folder and reading each parquet file
all_files = list_parquet_files(bucket_name, prefix)
dfs = []
# In[]
for i, file_key in tqdm(enumerate(all_files)):
    dfs.append(read_parquet_from_s3(bucket_name, file_key))

# Concatenate all dataframes and remove duplicates
big_dataframe =reduce(lambda x, y: x.union(y), dfs)

