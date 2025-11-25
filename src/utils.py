import os
import sys
import pandas as pd
import numpy as np

import dill
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass   
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    """Saves a Python object to a file using pickle."""
    try:
        
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)
    
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params=None) -> dict:
    """Evaluates multiple machine learning models and returns their R2 scores."""
    try:
        report = {}
        
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(X_train, y_train)
            params_i = params.get(list(models.keys())[i], None) if params else None
            
            if params_i:
                gs = GridSearchCV(model, params_i, cv=3, n_jobs=-1, verbose=2)
                gs.fit(X_train, y_train) 
                gs_best = gs.best_estimator_
                model = gs_best
                model.fit(X_train, y_train)
                
            else:
                model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score, gs.best_params_ if params_i else {}
            
        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    """Loads a Python object from a file using pickle."""
    
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)