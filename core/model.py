import warnings
import pickle
import os

import pretty_errors
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from sklearn.metrics import classification_report, confusion_matrix

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

from xgboost import XGBClassifier, plot_tree as plot_xgb
import matplotlib.pyplot as plt

warnings.filterwarnings(action='ignore')
curr_path = os.getcwd()

class HeartAttackModel():
    def __init__(self, X, y, **params) -> None:
        self.X = X
        self.y = y
        self.core_model = self.__build_model(**params)

    def __model_preprocess(self) -> tuple:

        categorical_features, numerical_features = [], []

        for feature, feature_type in zip(self.X.columns.to_list(), self.X.dtypes.to_list()):
            if feature_type == 'object':
                categorical_features.append(feature)
            else:
                numerical_features.append(feature)
        
        with open(os.path.join(curr_path, 'outputs', 'cache', 'features.pkl'), 'wb') as file_obj:
            pickle.dump((categorical_features, numerical_features), file_obj)
        
        return (categorical_features, numerical_features)

    def __build_model(self, **params) -> ImbPipeline:
        categorical_features, numerical_features = self.__model_preprocess()

        numerical_transformer = ImbPipeline(
            steps=[
                ("imputer", SimpleImputer(strategy='mean')),
                ("quantile_transformer", QuantileTransformer(n_quantiles=50))
            ]
        )

        categorical_transformer = ImbPipeline(
            steps=[
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ("selector", SelectPercentile(chi2, percentile=50))
            ]
        )
        preprocessor = ColumnTransformer(
            transformers=[
                ("numerical", numerical_transformer, numerical_features),
                ("categorical", categorical_transformer, categorical_features)
            ]
        )

        model = ImbPipeline([
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=12333)),
            ('classifier', XGBClassifier(**params))
        ])

        return model
    
    def train(self):
        self.core_model.fit(self.X, self.y)
    
    def predict(self, X):
        return self.core_model.predict(X)
    
    def score(self, X, y):
        return self.core_model.score(X, y)
    
    def evaluate(self, X, y) -> tuple:
        y_pred = self.core_model.predict(X)

        report = classification_report(y, y_pred)
        conf_matrix = confusion_matrix(y, y_pred)

        return (report, conf_matrix)
    
    def plot_tree(self):
        xgb_classifier = self.core_model.named_steps['classifier']
        model = xgb_classifier.get_booster()
        plot_xgb(model, num_trees=0, rankdir='TB')
        plt.savefig(os.path.join(curr_path, 'outputs', 'xgb_models', 'tree_model.png'), dpi=2400)
        plt.show()
    
    def save(self):
        with open(os.path.join(curr_path, 'outputs', 'xgb_models', 'best_model.pkl'), 'wb') as file_obj:
            pickle.dump(self.core_model, file_obj)

if __name__ == '__main__':
    pass