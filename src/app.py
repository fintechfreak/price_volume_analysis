import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("Price and volume analysis")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file...", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Check file type and read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        # Display the dataframe
        st.write(df)
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV or XLSX file.")

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the sample data file
sample_file = os.path.join(current_dir, '..', 'data', 'sample_data.csv')

# Load the sample data
try:
    df = pd.read_csv(sample_file)
    st.write("Sample Data:")
    st.write(df)
except FileNotFoundError:
    st.error("Sample data file not found. Please ensure it exists.")
