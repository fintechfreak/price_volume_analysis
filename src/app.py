import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("Price and Volume Analysis")

# Introduction with download link and required columns
st.markdown("""
### What You Can Do
You can download OHLCV (Open, High, Low, Close, Volume) data for various financial instruments from the following link for free (no registration required)
[Download Historical Data](https://www.dukascopy.com/trading-tools/widgets/quotes/historical_data_feed)
and then upload it here and the app will allow you to:
- **Clean the data**: 
    - Check if all required columns are present in the dataset
    - Remove any rows with missing values (NaN)
    - Convert Local/Gmt time column to a timestamp format
    - Convert OHLCV values to numeric format and round them to appropriate decimal places
    - Show simple statistics for the OHLCV columns
- **Analyze the data further** (coming soon)

The uploaded file should contain the following columns (you should be able to download any instrument with any parameter from the above link except for the Ticks parameter as it does not contain OHLCV data):
- **Local/Gmt time**: The timestamp of the data entry
- **Open**: The opening price
- **High**: The highest price
- **Low**: The lowest price
- **Close**: The closing price
- **Volume**: The trading volume

**Note**: Please see below "Clean Data" button. Clicking this button will clean your data according to the rules mentioned above, and the cleaned data will be displayed alongside the original data. Make sure to check this button after uploading your data or even now using sample data!
""")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the sample data file
sample_file = os.path.join(current_dir, '..', 'data', 'sample_data.csv')

# Load the sample data
try:
    sample_df = pd.read_csv(sample_file)
    # Initialize df with sample data
    df = sample_df
except FileNotFoundError:
    st.error("Sample data file not found. Please ensure it exists.")

# Section header for file upload
st.header("Upload Your Data")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file...", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Check file type and read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file) 
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV or XLSX file.")

# Button to clean data
clean_button_clicked = st.button("Clean Data")

if clean_button_clicked:
    if df is not None:
        # Data cleaning
        # Check if the required columns are present
        time_column_present = any("time" in col.lower() for col in df.columns)
        if not time_column_present:
            st.error("Missing a column with 'time' in its name.")

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Missing column: {col}")

        # Handle NaN values by dropping them
        # Before cleaning, count NaN values
        nan_count_before = df.isnull().sum().sum()

        # Remove rows with NaN values
        df_cleaned = df.dropna()

        # After cleaning, count NaN values
        nan_count_after = df_cleaned.isnull().sum().sum()
        rows_removed = nan_count_before - nan_count_after
        
        # Rename column with 'time' and convert it to timestamp format
        time_column = 'Local time' if 'Local time' in df_cleaned.columns else 'Gmt time'
        if time_column == 'Local time':
            df_cleaned[time_column] = pd.to_datetime(df_cleaned[time_column].str.replace(r' GMT[+-]\d{4}', '', regex=True), format='%d.%m.%Y %H:%M:%S.%f', errors='coerce')
        else:
            df_cleaned[time_column] = pd.to_datetime(df_cleaned[time_column], format='%d.%m.%Y %H:%M:%S.%f', errors='coerce')

        # Ensure OHLCV values are in numeric format with appropriate decimal places
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
            df_cleaned[col] = df_cleaned[col].round(2)  # Round to 2 decimal places for currency
        
        # Display the cleaned dataframe and the number of NaN values removed
        st.success(f"""
Checked if all required columns are present in dataset.\n
{rows_removed} rows removed due to NaN values.\n
Converted Local/Gmt time column to timestamp format.\n
Formatted OHLCV values to numeric format with 2 decimal places."""
    )
        # Use ternary operator to set the subheader text for cleaned data
        st.subheader("Cleaned uploaded data" if uploaded_file else "Cleaned sample data")
        st.write(df_cleaned)
        
        # Calculate statistics for OHLCV columns
        df_analyzed = df_cleaned[['Open', 'High', 'Low', 'Close', 'Volume']].agg(['mean', 'min', 'max', 'std'])
        
        # Display the statistics
        st.subheader("Cleaned uploaded data stats" if uploaded_file else "Cleaned sample data stats")
        st.write(df_analyzed)
    else:
        st.error("No data available to clean. Please upload a file or use the sample data.")

# Use ternary operator to set the subheader text
subheader_text = "Raw uploaded data" if uploaded_file else "Raw sample data"
st.subheader(subheader_text)

# Display the original dataframe
st.write(df)
