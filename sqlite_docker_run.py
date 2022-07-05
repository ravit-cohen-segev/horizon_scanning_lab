# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
import numpy as np
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

path = r"C:\Users\97252\Documents\Ravit\horizon_scanning_lab\example"
    
df = pd.read_csv(path)
#drop Unnamed column
#df.drop('Unnamed: 0', axis=1, inplace=True)

#name columns the same names as in db
cols = ['ID', 'col1', 'col2', 'col3','col4', 'col5']
df.columns = cols

#create table if doesn't exist
table_name = 'test_table'
table_cols ='(ID int NOT NULL PRIMARY KEY, col1 int, col2 int, col3 int, col4 int, col5 int)'
engine.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table_name, table_cols))

#convert to sql and  import into the temporary table
sql_file = df.to_sql(table_name, connection, if_exists='append', index=False)

#%% create new df for updating the existing table in df

df2 = pd.DataFrame(np.random.rand(3,6), columns=cols)
df2['ID'] = np.array([1,3,7])

#create temp table
temp_table = 'temp_table'

temp_table_cols ='(ID int NOT NULL PRIMARY KEY, col2 int)'

engine.execute("CREATE TABLE IF NOT EXISTS {} {}".format(temp_table, table_cols))

#insert new data into temp table. replace existing rows with new values

sql1 = "UPDATE {} AS t1 JOIN {} as t2 SET t1.col1 = t2.col1, \
    t1.col2 = t2.col2, t1.col3 = t2.col3, t1.col4 = t2.col4, t1.col5 = t2.col5 \
        WHERE t2.ID = t1.ID".format(table_name, temp_table)

engine.execute(sql1)
      
#remove the same rows from temp_table 
#sql2 = "DELETE FROM t2 WHERE t2.ID = t1.ID"

#JOIN tables


#engine.execute()
