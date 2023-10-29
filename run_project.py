import warnings
import time
import os

import pandas as pd
import optuna

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pretty_errors

from core.model import HeartAttackModel
from core.tune import HeartAttackTuner
from core.metrics import Metrics

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

def tune_model(num_trials: int):
    tuner = HeartAttackTuner()
    tuner.tune(n_trials=num_trials)
    return tuner.get_tuned_params()

def build_and_train_model(X_train, y_train, **params):
    model = HeartAttackModel(X_train, y_train, **params)
    model.train()
    return model

if __name__ == '__main__':
    print(f'\nReading data from csv...')
    time.sleep(1)
    X_train, X_test, y_train, y_test = get_data()
    print(f'Done')
    time.sleep(1)
    print(f'Read {len(y_train)+len(y_test)} record(s) from csv\n')
    time.sleep(1)

    n_trials = input("Number of trials to tune : ").strip()
    try:
        n_trials = int(n_trials)
    except:
        raise Exception("Input an integer")

    print(f"Tuning model for {n_trials} trial(s)...\n")
    best_params = tune_model(n_trials)
    print(f"Done\n")
    time.sleep(3)
    print(f"Best Hyperparameters:\n{best_params}\n")
    time.sleep(1)

    print(f'Training model ...')
    time.sleep(3)
    model = build_and_train_model(X_train, y_train, **best_params)
    model.save()
    print('Done\n')
    time.sleep(1)

    y_pred = model.predict(X_test)

    metrics = Metrics(y_true=y_test, y_pred=y_pred)

    print('Final Classification Report:')
    print(metrics.report())

    plot_conf_matrix = input("Display confusion matrix? [Y/n] : ").strip().lower()
    if plot_conf_matrix not in {'n', 'no'}:
        print("Confusion matrix displayed")
        metrics.plot_conf_matrix()
    
    plot_model = input("Display model? [Y/n] : ").strip().lower()
    if plot_model not in {'n', 'no'}:
        print("Model displayed")
        model.plot_tree()
    print()
