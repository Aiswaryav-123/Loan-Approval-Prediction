import streamlit as st
import pandas as pd
import joblib

# Load the pre-trained model
model = joblib.load('model.pkl')

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #003366;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 1.5em;
            color: #003366;
            margin-bottom: 20px;
        }
       
        .input-field {
            margin-bottom: 20px;
        }
        .button {
            background-color: #193de0
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            text-align: center;
        },
        .button:hover {
            background-color: #0056b3;
        }
        .result {
            text-align: center;
            margin-top: 20px;
            color: #003366;
        }
        .css-1r6slb0 {  
            background-color: #f8f9fa;  
            border-color: #007bff;      
        }
        .css-1p1l6y5 { 
            background-color: #f8f9fa;  
            border-color: #007bff;      
        }
        .css-1n8d2r4 {  
            background-color: #007bff; 
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)


st.markdown('<div class="title">Loan Eligibility Prediction</div>', unsafe_allow_html=True)

st.write("Enter your details below to check your loan eligibility.")
st.markdown('<div class="panel">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender:", ["Male", "Female"], key="gender")
    married = st.selectbox("Married:", ["Yes", "No"], key="married")
    dependents = st.selectbox("Dependents:", ["0", "1", "2", "3+"], key="dependents")
    education = st.selectbox("Education:", ["Graduate", "Not Graduate"], key="education")
    self_employed = st.selectbox("Self Employed:", ["Yes", "No"], key="self_employed")

with col2:
    applicant_income = st.number_input("Applicant Income:", min_value=0, value=5000, key="applicant_income")
    coapplicant_income = st.number_input("Coapplicant Income:", min_value=0, value=2000, key="coapplicant_income")
    loan_amount = st.number_input("Loan Amount:", min_value=0, value=100, key="loan_amount")
    loan_amount_term = st.number_input("Loan Amount Term (in days):", min_value=0, value=360, key="loan_amount_term")
    credit_history = st.selectbox("Credit History:", [0, 1], key="credit_history")
    property_area = st.selectbox("Property Area:", ["Urban", "Rural", "Semiurban"], key="property_area")

st.markdown('</div>', unsafe_allow_html=True)
gender = 1 if gender == 'Male' else 0
married = 1 if married == 'Yes' else 0
property_area = 0 if property_area == 'Rural' else 1 if property_area == 'Semiurban' else 2
self_employed = 1 if self_employed == 'Yes' else 0
education = 1 if education == 'Graduate' else 0
dependents = int(dependents)  


if st.button("Predict"):
    # Create a DataFrame with the input data
    data = {
        'Gender': [gender],
        'Married': [married],
        'Dependents': [dependents],
        'Education': [education],
        'Self_Employed': [self_employed],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [property_area]
    }
    input_df = pd.DataFrame(data)

    # Make prediction
    try:
        prediction = model.predict(input_df)
        # Display result
        if prediction[0] == 1:
            st.markdown('<div class="result"><p style="color: #28a745;">Loan Approved</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result"><p style="color: #dc3545;">Loan Not Approved</p></div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown('<div class="result"><p style="color: #dc3545;">An error occurred: {}</p></div>'.format(e), unsafe_allow_html=True)

