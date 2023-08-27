import streamlit as st
import pandas as pd
import requests
import xgboost as xgb
import tempfile

# Fetch the model from GitHub
response = requests.get('https://raw.githubusercontent.com/rudydesplan/book_rating/main/model/xgb_jsonFormat.json')
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
    st.write('Data Preview:')
    st.write(data.head())

    # Make predictions
    predictions = make_predictions(data)

    st.write('Predictions:')
    st.write(predictions)
