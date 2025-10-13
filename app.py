import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ICU Antibiotic Tracking",
    page_icon="💊",
    layout="wide"
)

# Google Sheets connection with better error handling
@st.cache_resource
def get_google_sheet_client():
    """Initialize and return Google Sheets client"""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Check if secrets exist
        if "gcp_service_account" not in st.secrets:
            st.error("❌ Google Cloud credentials not found in secrets!")
            return None, "Missing gcp_service_account in secrets"
        
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        client = gspread.authorize(credentials)
        return client, None
        
    except KeyError as e:
        error_msg = f"Missing key in secrets: {e}"
        st.error(f"❌ Configuration Error: {error_msg}")
        return None, error_msg
    except Exception as e:
        error_msg = f"Authentication error: {str(e)}"
        st.error(f"❌ {error_msg}")
        return None, error_msg

def get_sheet_id():
    """Extract Sheet ID from secrets"""
    try:
        if "sheets" not in st.secrets or "url" not in st.secrets["sheets"]:
            return None, "Sheet URL not configured in secrets"
        
        sheet_url = st.secrets["sheets"]["url"]
        
        # Extract ID from URL if it's a full URL
        if "docs.google.com/spreadsheets" in sheet_url:
            if "/d/" in sheet_url:
                sheet_id = sheet_url.split("/d/")[1].split("/")[0]
            else:
                return None, "Invalid Sheet URL format"
        else:
            # Assume it's already just the ID
            sheet_id = sheet_url
        
        return sheet_id, None
        
    except Exception as e:
        return None, f"Error extracting Sheet ID: {str(e)}"

def read_sheet(sheet_id, worksheet_name="Sheet1"):
    """Read data from Google Sheet"""
    try:
        client, error = get_google_sheet_client()
        if error:
            return None, error
        
        if not sheet_id:
            return None, "Sheet ID is empty"
        
        # Try to open the spreadsheet
        try:
            sheet = client.open_by_key(sheet_id)
        except gspread.exceptions.SpreadsheetNotFound:
            return None, f"Spreadsheet not found. Please verify:\n1. Sheet ID is correct: {sheet_id}\n2. Sheet is shared with service account"
        except gspread.exceptions.APIError as e:
            return None, f"Google API Error: {str(e)}"
        
        # Try to get the worksheet
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            return None, f"Worksheet '{worksheet_name}' not found. Available worksheets: {[ws.title for ws in sheet.worksheets()]}"
        
        # Get all records
        data = worksheet.get_all_records()
        
        if not data:
            return pd.DataFrame(), None
        
        return pd.DataFrame(data), None
        
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def append_to_sheet(sheet_id, row_data, worksheet_name="Sheet1"):
    """Append a row to Google Sheet"""
    try:
        client, error = get_google_sheet_client()
        if error:
            return False, error
        
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        worksheet.append_row(row_data)
        
        return True, None
        
    except gspread.exceptions.SpreadsheetNotFound:
        return False, "Spreadsheet not found"
    except gspread.exceptions.WorksheetNotFound:
        return False, f"Worksheet '{worksheet_name}' not found"
    except Exception as e:
        return False, f"Error appending data: {str(e)}"

def initialize_sheet_if_empty(sheet_id, worksheet_name="Sheet1"):
    """Initialize sheet with headers if empty"""
    try:
        client, error = get_google_sheet_client()
        if error:
            return False, error
        
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        
        # Check if sheet is empty
        if not worksheet.get_all_values():
            headers = ["Patient ID", "Antibiotic", "Dosage", "Date", "Time", "Added By"]
            worksheet.append_row(headers)
            return True, "Headers added successfully"
        
        return True, None
        
    except Exception as e:
        return False, f"Error initializing sheet: {str(e)}"

# Main app
st.title("💊 ICU Antibiotic Tracking System")

# Configuration section
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Get Sheet ID
    sheet_id, sheet_error = get_sheet_id()
    
    if sheet_error:
        st.error(f"❌ {sheet_error}")
        st.stop()
    
    st.success("✅ Sheet ID loaded")
    st.code(sheet_id, language=None)
    
    # Display service account email
    try:
        service_account_email = st.secrets["gcp_service_account"]["client_email"]
        st.info(f"**Service Account:**")
        st.code(service_account_email, language=None)
        
        st.warning("⚠️ **Setup Checklist:**")
        st.markdown("""
        1. ✓ Google Sheets API enabled
        2. ✓ Google Drive API enabled
        3. ✓ Share Sheet with service account
        4. ✓ Grant Editor permissions
        """)
        
    except Exception as e:
        st.error(f"❌ Error reading service account: {e}")
    
    # Test connection button
    if st.button("🔍 Test Connection", use_container_width=True):
        with st.spinner("Testing connection..."):
            client, error = get_google_sheet_client()
            if error:
                st.error(f"❌ Connection failed: {error}")
            else:
                st.success("✅ Connected successfully!")
                
                # Try to access the sheet
                df, read_error = read_sheet(sheet_id)
                if read_error:
                    st.error(f"❌ Cannot access sheet: {read_error}")
                else:
                    st.success("✅ Sheet accessible!")
    
    # Initialize sheet button
    if st.button("🔄 Initialize Sheet Headers", use_container_width=True):
        success, msg = initialize_sheet_if_empty(sheet_id)
        if success:
            st.success("✅ Sheet initialized!")
            if msg:
                st.info(msg)
        else:
            st.error(f"❌ {msg}")

# Main content area
st.divider()

# Read and display data
st.subheader("📊 Current Entries")

with st.spinner("Loading data from Google Sheets..."):
    df, error = read_sheet(sheet_id)

if error:
    st.error(f"❌ Error loading data: {error}")
    st.info("💡 **Troubleshooting Tips:**")
    st.markdown("""
    1. Verify the Google Sheet is shared with the service account email (shown in sidebar)
    2. Make sure the Sheet ID is correct
    3. Check that the sheet has a worksheet named 'Sheet1'
    4. Click 'Test Connection' in the sidebar to diagnose the issue
    """)
else:
    if df.empty:
        st.info("📝 No entries yet. Add your first entry below!")
        st.info("💡 Tip: Click 'Initialize Sheet Headers' in the sidebar if the sheet is empty")
    else:
        st.dataframe(df, use_container_width=True, height=400)
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total Entries", len(df))
        with col2:
            if "Antibiotic" in df.columns:
                st.metric("💊 Unique Antibiotics", df["Antibiotic"].nunique())
        with col3:
            if "Patient ID" in df.columns:
                st.metric("👤 Unique Patients", df["Patient ID"].nunique())
        with col4:
            if "Date" in df.columns:
                st.metric("📅 Latest Entry", df["Date"].max() if not df["Date"].empty else "N/A")

# Add new entry form
st.divider()
st.subheader("➕ Add New Entry")

with st.form("add_entry", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patient_id = st.text_input("Patient ID*", placeholder="e.g., ICU-001")
        antibiotic = st.text_input("Antibiotic*", placeholder="e.g., Ceftriaxone")
    
    with col2:
        dosage = st.text_input("Dosage*", placeholder="e.g., 1g IV")
        date = st.date_input("Date*")
    
    with col3:
        time = st.time_input("Time*")
        added_by = st.text_input("Added By", placeholder="Your name")
    
    col_submit1, col_submit2 = st.columns([3, 1])
    with col_submit2:
        submitted = st.form_submit_button("✅ Submit Entry", use_container_width=True, type="primary")
    
    if submitted:
        # Validate required fields
        if not patient_id or not antibiotic or not dosage:
            st.error("⚠️ Please fill in all required fields (marked with *)")
        else:
            with st.spinner("Adding entry..."):
                row_data = [
                    patient_id,
                    antibiotic,
                    dosage,
                    str(date),
                    str(time),
                    added_by if added_by else "Unknown"
                ]
                
                success, error = append_to_sheet(sheet_id, row_data)
                
                if success:
                    st.success("✅ Entry added successfully!")
                    st.balloons()
                    # Refresh the page to show new data
                    st.rerun()
                else:
                    st.error(f"❌ Failed to add entry: {error}")

# Footer
st.divider()
st.caption("💊 ICU Antibiotic Tracking System | Data stored securely in Google Sheets")
