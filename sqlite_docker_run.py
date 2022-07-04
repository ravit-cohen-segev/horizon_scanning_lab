# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
import mysql.connector as msql
from mysql.connector import Error
import sqlalchemy as db


#%% Connect to database created in mysql workbench

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'my-secret-pw',
    'database': 'mysqldb'   
}
 
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'# connect to database
engine = db.create_engine(connection_str)
connection = engine.connect()# pull metadata of a table
metadata = db.MetaData(bind=engine)
metadata.reflect(only=['test_table'])

test_table = metadata.tables['test_table']

#%% Read an example csv file I manually created and import csv into sql database

path = r"C:\Users\97252\Documents\Ravit\example"
    
df = pd.read_csv(path)
#drop Unnamed column
df.drop('Unnamed: 0', axis=1, inplace=True)

#name columns the same names as in db
cols = ['col1', 'col2', 'col3','col4', 'col5']
df.columns = cols

#convert to sql
sql_file = df.to_sql('test_table',connection, if_exists='append', index=False) 

