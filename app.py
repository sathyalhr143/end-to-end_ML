import pickle
# from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd 
from fastapi import FastAPI
from pydantic import BaseModel

from sklearn.preprocessing import StandardScaler


from src.utils import load_object
# from src.components.main import model_name, best_model, r2_score, model_params

from src.exception import CustomException
from src.logger import logging
import sys
import os
from src.pipelines.predict_pipeline import PredictPipeline, CustomData


application = FastAPI()

class Datapoint(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    writing_score: float # value should be between 0-100
    reading_score: float # value should be between 0-100
    
    
    class Config:
        json_schema_extra = {
            "example": {
                'gender': 'female/male',
                'race_ethnicity': 'group A/B/C/D/E',
                'parental_level_of_education': "bachelor's degree/some college/master's degree/associate's degree/high school/some high school",
                'lunch': 'standard/free/reduced',
                'test_preparation_course': 'none/completed',
                'writing_score': 72.0, #any int/float between 0-100
                'reading_score': 74.0 #any int/float between 0-100
            }
        }   


# Route for home page
@application.get('/')
def index():
    return {"message": "Welcome to the Machine Learning Model Trainer"}

# Route for prediction
@application.post('/predict')
async def predict_datapoint(data: Datapoint):
    try:
        data_point = CustomData(
            gender=data.gender,
            race_ethnicity=data.race_ethnicity,
            parental_level_of_education=data.parental_level_of_education,
            lunch=data.lunch,
            test_preparation_course=data.test_preparation_course,
            writing_score=float(data.writing_score),
            reading_score=float(data.reading_score)
        )
        
        
        pred_df = data_point.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict_pipe(pred_df)
        return {"prediction math Score": prediction.tolist()}
        
    except Exception as e:
        raise CustomException(e, sys)
