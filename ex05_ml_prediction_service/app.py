import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

import os
import sys

LOAD_PATH = "models/random_forest_model.joblib"

if not os.path.exists(LOAD_PATH):
    print(f"{LOAD_PATH} does not exist! Verify if your trained a usable model in: machine_learning.py")
    sys.exit(1)

model:RandomForestRegressor = joblib.load(LOAD_PATH)

# Streamlit app title
st.title("RandomForest Prediction App")

# Input fields for features
st.header("Enter Feature Values")
feature1 = st.number_input("Feature 1", value=0.0)
feature2 = st.number_input("Feature 2", value=0.0)
feature3 = st.number_input("Feature 3", value=0.0)

# Button to trigger prediction
if st.button("Predict"):
    # Prepare input data as a DataFrame (adjust column names as needed)
    input_data = pd.DataFrame({
        'feature1': [feature1],
        'feature2': [feature2],
        'feature3': [feature3]
    })
    # Make prediction
    prediction = model.predict(input_data)
    st.subheader("Prediction Result")
    st.write(f"The predicted class is: {prediction[0]}")

# Possible autres features
#feature1 = st.slider("Feature 1", min_value=0, max_value=100, value=50)
#feature2 = st.selectbox("Feature 2", ["Option 1", "Option 2"])
