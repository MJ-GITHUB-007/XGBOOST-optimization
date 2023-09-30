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

class Model:
    def __init__(self) -> None:
        self.curr_path = os.getcwd()
        self.data = None

        self.core = Pipeline([
            ('data_transformer', QuantileTransformer()),
            ('xgbclassifier', XGBClassifier())
        ])
    
    def __get_data(self) -> np.ndarray:
        print(f'Reading data from csv')
        time.sleep(2)
        data = pd.read_csv(os.path.join(self.curr_path, 'data_xgb.csv'))
        print(f'Done')
        print(f'Read {len(data)} record(s) from csv\n')
        return np.array(data)
    
    def __split_data(self) -> None:
        row_size = len(self.data[0])-1
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data[:,:row_size], self.data[:,-1], test_size=0.05, shuffle=True)

    def train(self) -> None:
        self.data = self.__get_data()

        print(f'Training model ...')
        self.__split_data()
        time.sleep(3)
        self.core.fit(self.X_train, self.y_train)
        print('Model trained')
        time.sleep(1)

        with open(os.path.join(self.curr_path, 'models/cc_fraud_detector.pkl'), 'wb') as f_obj:
            pickle.dump(self, f_obj)
            print(f'Model saved\n')
    
    def predict(self, data) -> np.ndarray:
        predictions = self.core.predict(data)
        predictions = np.array(predictions)
        return predictions

if __name__ == '__main__':
    model = Model()
    model.train()