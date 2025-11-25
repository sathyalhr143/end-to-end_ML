from src. components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
import sys
import os

from src.exception import CustomException   
from src.logger import logging

def main():
    data_injestion = DataIngestion()
    train_path, test_path = data_injestion.initiate_data_ingestion(path='notebook/data/student.csv')
    
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_path, test_path)
    
    model_trainer = ModelTrainer()
    model_name, model, r2_score, model_params = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"Best Model: {model_name} with a R2 Score: {r2_score} and Parameters: {model_params}")
    
if __name__== "__main__":
    try: 
        main()
        
    except Exception as e:
        raise CustomException(e, sys)