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
from congigs import SQL_configs
configs = SQL_configs()
curr_path = os.getcwd()

# csv file name
filename = os.path.join(curr_path, '../data_xgb.csv')

# initializing the titles list
fields = []
data = []
limit = 0

connection =  mysql.connector.connect(
        host=configs.host,
        user=configs.user,
        password=configs.passwd,
        database=configs.database,
        auth_plugin=configs.auth_plugin
    )
try:
    initial_query = """
    DROP TABLE credit_card_fraud;
    """
    # Drop the table
    cursor = connection.cursor()
    cursor.execute(initial_query)
    cursor.close()
    print('Dropped existing table credit_card_fraud')
except:
    print('No existing table found')

initial_query = """
CREATE TABLE credit_card_fraud(
ID MEDIUMINT,
V1 DECIMAL(24, 20),
V2 DECIMAL(24, 20),
V3 DECIMAL(24, 20),
V4 DECIMAL(24, 20),
V5 DECIMAL(24, 20),
V6 DECIMAL(24, 20),
V7 DECIMAL(24, 20),
V8 DECIMAL(24, 20),
V9 DECIMAL(24, 20),
V10 DECIMAL(24, 20),
V11 DECIMAL(24, 20),
V12 DECIMAL(24, 20),
V13 DECIMAL(24, 20),
V14 DECIMAL(24, 20),
V15 DECIMAL(24, 20),
V16 DECIMAL(24, 20),
V17 DECIMAL(24, 20),
V18 DECIMAL(24, 20),
V19 DECIMAL(24, 20),
V20 DECIMAL(24, 20),
V21 DECIMAL(24, 20),
V22 DECIMAL(24, 20),
V23 DECIMAL(24, 20),
V24 DECIMAL(24, 20),
V25 DECIMAL(24, 20),
V26 DECIMAL(24, 20),
V27 DECIMAL(24, 20),
V28 DECIMAL(24, 20),
Amount DECIMAL(10, 2),
Class TINYINT,
PRIMARY KEY (ID)
);
"""
# Initialize the table
time.sleep(2)
cursor = connection.cursor()
cursor.execute(initial_query)
cursor.close()
connection.close()
print('Created table credit_card_fraud')
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
                    insert_query = "INSERT INTO credit_card_fraud (ID, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    # Insert data into the table
                    cursor.executemany(insert_query, data)
                    print(f'{i+1} record(s) inserted')
                    # Commit the changes to the database
                    connection.commit()

                    data = []

print(f'Done')
