import streamlit as st

from src.exception import CustomException
from src.logger import logging
from src.pipelines.predict_pipeline import CustomData, PredictPipeline
import sys
import os

import pandas as pd
import numpy as np


# set up the pafe configuration
st.set_page_config(page_title="Student Performance Prediction", page_icon=":bar_chart:", layout="centered")

# Title of the web app
st.title("Student Performance Prediction App")
st.markdown("Provide the student's details to below to predict their **math score**. :point_down:")

with st.form(key='prediction_form'):
    
    # Creating two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox(
            "Gender",
            options=["female", "male"]
        )
        
        race_ethnicity = st.selectbox(
            "Race/Ethnicity", 
            options=["group A", "group B", "group C", "group D", "group E"]
        )
        
        parental_level_of_education = st.selectbox(
            "Parental Level of Education",
            options=[
                "bachelor's degree",
                "some college",
                "master's degree",
                "associate's degree",
                "high school",
                "some high school"
            ]
        )   
        
        lunch = st.selectbox(
            "Lunch",
            options=["standard", "free/reduced"]
        )
        
        test_preparation_course = st.selectbox(
            "Test Preparation Course",
            options=["none", "completed"]
        )
        
    with col2:
        writing_score = st.number_input(
            "Writing Score (0-100)",
            min_value=0.0,
            max_value=100.0,
            step=0.1
        )
        
        reading_score = st.number_input(
            "Reading Score (0-100)",
            min_value=0.0,
            max_value=100.0,
            step=0.1
        )
        
    # Submit button
    submit_button = st.form_submit_button(label='Predict Math Score')
    
    
# Logic When the submit button is clicked 
if submit_button:
    
    try:
        # Create an instance of CustomData
        data_point = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            writing_score=writing_score,
            reading_score=reading_score 
        )
        
        
        
        #get the data as a dataframe
        pred_df = data_point.get_data_as_data_frame()
        
        # write input data to the app
        st.subheader("Input Student Details:")
        st.dataframe(pred_df)
        
        # Run the prediction pipeline
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict_pipe(pred_df)
        
        
        st.success(f"The predicted math score is: {prediction[0]:.2f}")
        
        # Celebrate if the predicted score is high
        if prediction[0] >= 80:
            st.write(f"🎉 Excellent performance predicted as {prediction[0]}! Keep it up! You are doing great 🎉")
            st.balloons()
            
        elif prediction[0] < 40:
            st.write(f"📚 Don't be discouraged by a predicted score of {prediction[0]:.2f}. \n \
                With dedication and hard work, you can improve your math skills! Keep pushing forward! 📚")
            
        else:
            st.write(f"👍 A predicted score of {prediction[0]:.2f} shows you're on the right track. \n \
                Keep practicing and striving for excellence! You've got this! 👍")
            st.snow()
    except Exception as e:
        
        st.error(f"Error in input data: {e}")
        sys.exit()