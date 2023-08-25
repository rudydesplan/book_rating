import streamlit as st
import pandas as pd
import requests
import xgboost as xgb
import tempfile
from preprocessing import preprocess_data

# Fetch the model from GitHub
response = requests.get('https://raw.githubusercontent.com/rudydesplan/book_rating/main/xgboost_model.json')
response.raise_for_status()  # Raise an exception for HTTP errors

# Create a temporary file to store the model
with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp:
    temp.write(response.content)
    temp_filename = temp.name

# Load the XGBoost model from the temporary file
model = xgb.Booster()
model.load_model(temp_filename)

def make_predictions(df):
    return model.predict(xgb.DMatrix(df))

# Title
st.title('XGBoost Model Predictor')

# Allow user to upload CSV
uploaded_file = st.file_uploader("Upload CSV file for predictions", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
    # Preprocess the data using the imported function
    preprocessed_data = preprocess_data(data)
    
    st.write('Data Preview:')
    st.write(preprocessed_data.head())

    # Make predictions
    predictions = make_predictions(preprocessed_data)

    st.write('Predictions:')
    st.write(predictions)