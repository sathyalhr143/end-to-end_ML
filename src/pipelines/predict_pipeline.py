import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import numpy as np
import pandas as pd


class PredictPipeline:
    def __init__(self):
        pass
    
    def predict_pipe(self, data):
        try:
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model_path = 'artifacts/model.pkl'
            
            preprocessor = load_object(file_path=preprocessor_path)
            model = load_object(file_path=model_path)
            
            processed_data = preprocessor.transform(data)
            preds = model.predict(processed_data)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)
    
class CustomData:
    def __init__(self,
                gender: str,
                race_ethnicity: str,
                parental_level_of_education: str,
                lunch: str,
                test_preparation_course: str,
                writing_score: float,
                reading_score: float):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.writing_score = writing_score
        self.reading_score = reading_score
        
        
        if self.writing_score < 0 or self.writing_score > 100:
            raise ValueError("writing_score must be between 0 and 100")
        if self.reading_score < 0 or self.reading_score > 100:
            raise ValueError("reading_score must be between 0 and 100")
        
        
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender" : [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "writing_score": [self.writing_score],
                "reading_score": [self.reading_score]
            }
            
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys)