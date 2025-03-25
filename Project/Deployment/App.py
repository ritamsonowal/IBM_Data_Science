import streamlit as st
import pandas as pd
import joblib

# Load the logistic regression model
model = joblib.load("logistic_model.joblib")

def calculate_bp_category(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return 1  # Normal
    elif 120 <= systolic < 130 and diastolic < 80:
        return 2  # Elevated
    else:
        return 3  # High

def convert_ft_to_cm(ft_in):
    try:
        feet, inches = map(int, ft_in.split('.'))
        return (feet * 30.48) + (inches * 2.54)
    except ValueError:
        return 0

st.markdown("<h1 style='text-align: center;'>Heart Disease Risk Predictor</h1>", unsafe_allow_html=True)
st.write("Enter your health details to predict the risk of heart disease.")

# User Inputs
smoke = st.selectbox("Do you smoke?", ["No", "Yes"])
smoke = 1 if smoke == "Yes" else 0

cholesterol = st.selectbox("Cholesterol Level", [
    "Healthy (Less than 200 mg/dL)",
    "Borderline High (200–239 mg/dL)",
    "High (240 mg/dL and above)"
])
cholesterol = {
    "Healthy (Less than 200 mg/dL)": 1,
    "Borderline High (200–239 mg/dL)": 2,
    "High (240 mg/dL and above)": 3
}[cholesterol]

col1, col2 = st.columns(2)
with col1:
    ap_hi = st.number_input("Enter Upper Blood Pressure (Systolic)", min_value=80, max_value=200, value=120)
with col2:
    ap_lo = st.number_input("Enter Lower Blood Pressure (Diastolic)", min_value=50, max_value=150, value=80)

age_years = st.number_input("Age (in years)", min_value=18, max_value=100, value=45)

weight = st.number_input("Enter Weight (in kg)", min_value=20.0, max_value=200.0, value=70.0)

ft_in = st.text_input("Enter Height (feet.inches)", value="5.7")

height = convert_ft_to_cm(ft_in)

# Automatically calculate blood pressure category
bp_category = calculate_bp_category(ap_hi, ap_lo)

# Predict Cardiac Risk
if st.button("Predict"):
    input_data = pd.DataFrame([[cholesterol, smoke, age_years, bp_category, ap_hi, ap_lo, weight, height]],
                              columns=['cholesterol', 'smoke', 'age_years', 'bp_category', 'ap_hi', 'ap_lo', 'weight', 'height'])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Disease!")
    else:
        st.success("✅ Low Risk of Heart Disease!")

st.markdown("<p style='text-align: center; color: gray;'>Note: This is just a prediction and not actual medical advice.</p>", unsafe_allow_html=True)