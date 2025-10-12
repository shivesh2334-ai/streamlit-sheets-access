import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

# Create a connection to Google Sheets
def get_google_sheet_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    
    client = gspread.authorize(credentials)
    return client

# Read data from Google Sheet
def read_sheet(sheet_url, worksheet_name="Sheet1"):
    client = get_google_sheet_client()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Write data to Google Sheet
def write_to_sheet(sheet_url, data, worksheet_name="Sheet1"):
    client = get_google_sheet_client()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(worksheet_name)
    
    # Clear existing data
    worksheet.clear()
    
    # Write headers and data
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())

# Append a row to Google Sheet
def append_to_sheet(sheet_url, row_data, worksheet_name="Sheet1"):
    client = get_google_sheet_client()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(worksheet_name)
    worksheet.append_row(row_data)

# Example usage in your app
st.title("ICU Antibiotic Tracking")

# Your Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# Read data
try:
    df = read_sheet(SHEET_URL)
    st.dataframe(df)
except Exception as e:
    st.error(f"Error reading sheet: {e}")

# Add new data
with st.form("add_entry"):
    st.subheader("Add New Entry")
    col1, col2 = st.columns(2)
    
    with col1:
        patient_id = st.text_input("Patient ID")
        antibiotic = st.text_input("Antibiotic")
    
    with col2:
        dosage = st.text_input("Dosage")
        date = st.date_input("Date")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        try:
            append_to_sheet(SHEET_URL, [patient_id, antibiotic, dosage, str(date)])
            st.success("Entry added successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error adding entry: {e}")
