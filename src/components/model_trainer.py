import pandas as pd
import numpy as np
import sys
import os
from dataclasses import dataclass   

from src.exception import CustomException
from src.logger import logging  
from src.utils import save_object, evaluate_models

from sklearn.model_selection import train_test_split


from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from xgboost import XGBRegressor


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing input data")
            X_train, y_train, X_test, y_test  = (train_array[:,:-1], train_array[:,-1],
                                                test_array[:,:-1], test_array[:,-1])
            
            models = {
                "Random Forest_100": RandomForestRegressor(n_estimators=100,n_jobs=-1),
                "Random Forest_50": RandomForestRegressor(n_estimators=50,n_jobs=-1),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": AdaBoostRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "SVR": SVR(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "KNeighbors Regressor": KNeighborsRegressor()
            }
            
            params = {
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter':['best', 'random'],
                    'max_features':['sqrt','log2',None]
                },
                "Random Forest": {
                    'n_estimators':[5, 10, 20, 50, 100, 125, 150, 200],
                    'max_features':['sqrt','log2',None]
                },
                
                "Gradient Boosting": {
                    'n_estimators':[5, 10, 20, 50, 100],
                    'learning_rate':[0.01, 0.1, 0.2]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'n_estimators':[10,20,50, 100],
                    'learning_rate':[0.01, 0.1, 0.2]
                },
                "CatBoosting Regressor": {
                    'iterations':[10, 20, 50, 100],
                    'learning_rate':[0.01, 0.1, 0.2]
                },
                "AdaBoost Regressor": {
                    'n_estimators':[10, 20, 50, 100],
                    'learning_rate':[0.01, 0.1, 0.2]
                },
                "SVR": {
                    'kernel':['linear', 'poly', 'rbf', 'sigmoid'],
                    'C':[0.1, 1, 10]
                },
                "Ridge": {
                    'alpha':[0.1, 0.5, 1,5, 10]
                },
                "Lasso": {
                    'alpha':[0.1, 0.5, 1,5, 10]
                },
                "KNeighbors Regressor": {
                    'n_neighbors':[3, 5, 7],
                    'weights':['uniform', 'distance']
                }
            }
            
            logging.info("Training and evaluating models")
            
            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models= models, params= params)
            
            best_model_score, best_model_params = max(sorted((score, params) for score, params in model_report.values()))
            
            best_model_name = list(model_report.keys())[
                list(score for score, params in model_report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]
            
            if best_model_score < 0.8:
                raise CustomException("No best model found")
            
            logging.info(f"Best model found: {best_model_name} with r2 score: {model_report[best_model_name]}")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            return best_model_name, best_model, best_model_score, best_model_params
            
        except Exception as e:
            raise CustomException(e, sys)