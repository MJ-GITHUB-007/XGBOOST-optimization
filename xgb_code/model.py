import numpy as np
import pandas as pd
import mysql.connector
import pickle
import time
import os
import warnings
warnings.filterwarnings(action='ignore')
import pretty_errors

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from SQL import SQL_configs, SQL_queries

class Model:
    def __init__(self) -> None:
        self.configs = SQL_configs()
        self.queries = SQL_queries()
        self.curr_path = os.getcwd()
        self.data = self.__get_data()
        self.core = XGBClassifier()
    
    def __get_data(self) -> np.ndarray:
        with mysql.connector.connect(
        host=self.configs.host,
        user=self.configs.user,
        password=self.configs.passwd,
        database=self.configs.database,
        auth_plugin=self.configs.auth_plugin
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.queries.select_query)
                print('Reading data from database')
                time.sleep(2)
                print('Please wait...')
                data = cursor.fetchall()
        print('Done')
        time.sleep(2)
        print(f'Read {len(data)} record(s) from database\n')
        return np.array(data)
    
    def __split_data(self) -> None:
        row_size = len(self.data[0])-1
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data[:,:row_size], self.data[:,-1], test_size=0.05, shuffle=True)

    def train(self) -> None:
        print(f'Training model ...')
        self.__split_data()
        time.sleep(3)
        self.core.fit(self.X_train, self.y_train)
        print('Model trained')
        time.sleep(1)

        with open(os.path.join(self.curr_path, 'models/cc_fraud_detector.pkl'), 'wb') as f_obj:
            pickle.dump(self, f_obj)
            print(f'Model saved')
    
    def predict(self, data) -> np.ndarray:
        predictions = self.core.predict(data)
        predictions = np.array(predictions)
        return predictions

if __name__ == '__main__':
    model = Model()
    model.train()