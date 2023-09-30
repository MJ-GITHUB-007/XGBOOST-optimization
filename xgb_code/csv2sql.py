import csv
import pandas as pd
from datetime import date
import mysql.connector
import time
import os
import warnings
warnings.filterwarnings(action='ignore')
import pretty_errors

# Importing and setting configurations
from SQL import SQL_configs, SQL_queries
configs = SQL_configs()
queries = SQL_queries()
curr_path = os.getcwd()

# csv file name
filename = os.path.join(curr_path, 'data_xgb.csv')

# initializing the titles list
fields = []
data = []
limit = 0

with mysql.connector.connect(
        host=configs.host,
        user=configs.user,
        password=configs.passwd,
        database=configs.database,
        auth_plugin=configs.auth_plugin
) as connection:
    try:
        # Drop the table
        with connection.cursor() as cursor:
            cursor.execute(queries.drop_query)
            print(f'Dropped existing table {configs.table}')
    except:
        print('No existing table found')

    # Initialize the table
    time.sleep(2)
    with connection.cursor() as cursor:
        cursor.execute(queries.initial_query)
print(f'Created table {configs.table}')
time.sleep(2)

with mysql.connector.connect(
    host=configs.host,
    user=configs.user,
    password=configs.passwd,
    database=configs.database,
    auth_plugin=configs.auth_plugin
) as connection:
    
    with connection.cursor() as cursor:

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            limit = sum(1 for row in csvreader)
            print(f'{limit} record(s) found in csv.')

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            print(f'Extracting data from csv to database.')
            print(f'Please wait...')

            # extracting each data row one by one
            for i, row in enumerate(csvreader):

                data_to_insert = (
                    int(row[0]),
                    round(float(row[1]), 20),
                    round(float(row[2]), 20),
                    round(float(row[3]), 20),
                    round(float(row[4]), 20),
                    round(float(row[5]), 20),
                    round(float(row[6]), 20),
                    round(float(row[7]), 20),
                    round(float(row[8]), 20),
                    round(float(row[9]), 20),
                    round(float(row[10]), 20),
                    round(float(row[11]), 20),
                    round(float(row[12]), 20),
                    round(float(row[13]), 20),
                    round(float(row[14]), 20),
                    round(float(row[15]), 20),
                    round(float(row[16]), 20),
                    round(float(row[17]), 20),
                    round(float(row[18]), 20),
                    round(float(row[19]), 20),
                    round(float(row[20]), 20),
                    round(float(row[21]), 20),
                    round(float(row[22]), 20),
                    round(float(row[23]), 20),
                    round(float(row[24]), 20),
                    round(float(row[25]), 20),
                    round(float(row[26]), 20),
                    round(float(row[27]), 20),
                    round(float(row[28]), 20),
                    round(float(row[29]), 2),
                    int(row[30]),
                )
                data.append(data_to_insert)
                if len(data) >= 20000 or i >= limit-1:
                    # Insert data into the table
                    cursor.executemany(queries.insert_query, data)
                    print(f'{i+1} record(s) inserted')
                    # Commit the changes to the database
                    connection.commit()

                    data = []

print(f'Done')
