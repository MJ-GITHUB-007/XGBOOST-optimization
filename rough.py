import pickle
from xgb_code.model import Model
    
if __name__ == '__main__':
    with open('models/cc_fraud_detector.pkl', 'rb') as f_obj:
        new = pickle.load(f_obj)
    
    new.train()