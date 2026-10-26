import streamlit as st
import joblib
import numpy as np

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="centered"
)

# -------------------------------
# Load Model
# -------------------------------
model = joblib.load("diabetes_model.pkl")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("📋 About")
st.sidebar.info(
    """
    **Diabetes Risk Prediction App**

    This application predicts whether a patient is likely to have diabetes
    using a Machine Learning model.

    **Outcome**
    - ✅ 0 = Not Diabetic
    - ❌ 1 = Diabetic
    """
)

# -------------------------------
# Main Title
# -------------------------------
st.title("🩺 Diabetes Risk Prediction")
st.markdown("---")

st.write(
    "Enter the patient's medical information below and click "
    "**Predict** to check the diabetes risk."
)

# -------------------------------
# Input Fields
# -------------------------------
st.subheader("📊 Patient Information")

# -------------------------------
# Two Column Layout
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col2:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )

# Show Pregnancies only for Female
if gender == "Female":
    preg = st.number_input(
        "Pregnancies",
        min_value=0,
        max_value=15,
        value=0,
        step=1
    )
else:
    preg = 0

glu = st.number_input(
    "Glucose (mg/dL)",
    min_value=0,
    max_value=300,
    value=120
)

bp = st.number_input(
    "Blood Pressure (mm Hg)",
    min_value=0,
    max_value=200,
    value=70
)

skin = st.number_input(
    "Skin Thickness (mm)",
    min_value=0,
    max_value=100,
    value=20
)

ins = st.number_input(
    "Insulin (mu U/ml)",
    min_value=0,
    max_value=900,
    value=80
)

bmi = st.number_input(
    "BMI",
    min_value=0.0,
    max_value=70.0,
    value=25.0
)

dpf = st.number_input(
    "Diabetes Pedigree Function",
    min_value=0.0,
    max_value=3.0,
    value=0.5
)

# Vlaidation of inputs
def validate_inputs():
    errors = []

    # Validate pregnancies only for females
    if gender == "Female":
        if preg < 0 or preg > 15:
            errors.append("❌ Pregnancies should be between 0 and 15.")

    # Validate all remaining fields for everyone
    if glu < 70 or glu > 200:
        errors.append("❌ Glucose should be between 70 and 200 mg/dL.")

    if bp < 40 or bp > 130:
        errors.append("❌ Blood Pressure should be between 40 and 130 mm Hg.")

    if skin < 7 or skin > 60:
        errors.append("❌ Skin Thickness should be between 7 and 60 mm.")

    if ins < 15 or ins > 400:
        errors.append("❌ Insulin should be between 15 and 400 mu U/ml.")

    if bmi < 15 or bmi > 50:
        errors.append("❌ BMI should be between 15 and 50.")

    if dpf < 0.05 or dpf > 2.5:
        errors.append("❌ Diabetes Pedigree Function should be between 0.05 and 2.5.")

    if age < 18 or age > 100:
        errors.append("❌ Age should be between 18 and 100 years.")

    return errors
# -------------------------------
# Prediction
# -------------------------------
if st.button("🔍 Predict Diabetes Risk"):

    validation_errors = validate_inputs()

    if validation_errors:
        st.error("⚠️ Invalid Input Detected!")

        for err in validation_errors:
            st.write(err)

        st.warning("Please correct the above values before making a prediction.")

    else:
        # Display entered information
        st.markdown("---")
        st.subheader("Patient Details")
        st.write(f"**Gender:** {gender}")

        data = np.array([[preg, glu, bp, skin, ins, bmi, dpf, age]])

        prediction = model.predict(data)

        st.markdown("---")

        if prediction[0] == 1:
            st.error("🔴 Prediction: Patient is likely Diabetic")

        else:
            st.success("🟢 Prediction: Patient is Not Diabetic")
