import streamlit as st
import pandas as pd

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