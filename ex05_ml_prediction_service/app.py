import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load your pre-trained RandomForest model
# model = joblib.load('your_model.pkl')  # Uncomment and replace with your model file

# Example: Create a dummy model if you don't have one yet
# (Replace this with your actual model loading code)
model = RandomForestClassifier(random_state=42)
# Assume you have trained your model and saved it as 'model.pkl'

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
