import numpy as np
import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load model
dt_classifier = joblib.load("Tree_classifier.sav")

# PROPERLY initialize and fit LabelEncoder with all 3 classes
label_encoder = LabelEncoder()
label_encoder.fit(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])

st.title("Enter Flower Measurements to predict the Iris species:")

# Input fields with default values
sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, max_value=10.0, value=5.1)
sepal_width = st.number_input("Sepal Width (cm)", min_value=0.0, max_value=10.0, value=3.5)
petal_length = st.number_input("Petal Length (cm)", min_value=0.0, max_value=10.0, value=1.4)
petal_width = st.number_input("Petal Width (cm)", min_value=0.0, max_value=10.0, value=0.2)

if st.button("Predict"):
    # Create DataFrame with correct column names
    input_features = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                                columns=['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'])
    
    # Get prediction and ensure it's a numpy array
    pred = dt_classifier.predict(input_features)
    
    # Convert prediction to proper format
    if isinstance(pred, list):
        pred = np.array(pred)
    
    # Inverse transform - no need for reshape if using correct format
    species = label_encoder.inverse_transform(pred)
    
    # Display result
    st.success(f"Predicted Species: **{species[0]}**")