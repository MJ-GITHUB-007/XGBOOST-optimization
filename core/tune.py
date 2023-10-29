import warnings
import pickle
import os

import pandas as pd
import optuna

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pretty_errors

from core.model import HeartAttackModel

warnings.filterwarnings(action='ignore')
curr_path = os.getcwd()

def get_data():
    X = pd.read_csv(os.path.join(curr_path, 'csv_data.csv'))
    X.dropna(inplace=True)
    X.drop_duplicates(inplace=True)
    X.drop('State', axis=1, inplace=True)

    label_encoder = LabelEncoder()
    y = X.pop('HadHeartAttack')
    y = label_encoder.fit_transform(y)

    return train_test_split(X, y, test_size=0.01, random_state=12333, stratify=y)

def objective(trial):

    params = {
        'n_estimators': trial.suggest_int('classifier__n_estimators', 50, 200),
        'max_depth': trial.suggest_int('classifier__max_depth', 3, 15),
        'learning_rate': trial.suggest_float('classifier__learning_rate', 0.001, 0.1, log=True),
        'subsample': trial.suggest_float('classifier__subsample', 0.5, 1.0),
        'gamma': trial.suggest_float('classifier__gamma', 0, 1),
        'colsample_bytree': trial.suggest_float('classifier__colsample_bytree', 0.5, 1.0)
    }

    model = HeartAttackModel(X_train, y_train, **params)
    model.train()

    return 1 - model.score(X_test, y_test)

X_train, X_test, y_train, y_test = get_data()

class HeartAttackTuner():
    def __init__(self) -> None:
        self.study = optuna.create_study(direction='minimize')

    def tune(self, n_trials: int):  
        self.study.optimize(objective, n_trials=n_trials)
    
    def get_tuned_params(self):
        with open(os.path.join(curr_path, 'outputs', 'cache', 'best_params.pkl'), 'wb') as file_obj:
            pickle.dump(self.study.best_params, file_obj)
        return self.study.best_params

if __name__ == '__main__':
    pass