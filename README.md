# ICU Antibiotic Tracking System

A Streamlit application for tracking and managing antibiotic administration in ICU settings, integrated with Google Sheets for real-time data storage and collaboration.

## Features

- 📊 Real-time antibiotic administration tracking
- 🔄 Google Sheets integration for data persistence
- 📝 Easy data entry and management
- 📈 Data visualization and reporting
- 🔒 Secure authentication using Google Service Accounts
- 💾 Automated data backup to cloud

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Google Sheets API enabled
- Streamlit Cloud account (for deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/icu-antibiotic-gs.git
cd icu-antibiotic-gs
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

### 4. Create Service Account Credentials

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in the service account details and create
4. Go to the **Keys** tab
5. Click **Add Key** > **Create New Key** > **JSON**
6. Download the JSON file (keep it secure!)

### 5. Configure Google Sheet

1. Create a new Google Sheet or use an existing one
2. Share the sheet with your service account email (found in the JSON file)
   - Email format: `your-service-account@your-project.iam.gserviceaccount.com`
3. Grant **Editor** permissions
4. Copy the Sheet URL

### 6. Set Up Local Secrets

Create a `.streamlit/secrets.toml` file in your project root:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

[sheets]
url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

**⚠️ Important:** Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent committing credentials.

## Running Locally

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

**Note:** Ensure `.streamlit/secrets.toml` is in your `.gitignore`

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select your repository, branch, and main file (`app.py`)
4. Click **Advanced settings**
5. Paste your secrets from `.streamlit/secrets.toml` into the **Secrets** field
6. Click **Deploy**

## Project Structure

```
icu-antibiotic-gs/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore file
│
└── .streamlit/
    └── secrets.toml           # Local secrets (not committed)
```

## Usage

### Adding New Entries

1. Fill in the patient information form
2. Select antibiotic and dosage details
3. Click **Submit** to save to Google Sheets

### Viewing Data

- The main dashboard displays all antibiotic administration records
- Use filters to search and sort data
- Export data for reports and analysis

### Data Management

- **Edit:** Click on any entry to modify details
- **Delete:** Remove entries with confirmation
- **Export:** Download data as CSV or Excel

## Configuration

### Google Sheet Structure

Your Google Sheet should have the following columns (customize as needed):

| Patient ID | Name | Antibiotic | Dosage | Route | Date | Time | Administered By | Notes |
|------------|------|------------|--------|-------|------|------|-----------------|-------|

### Customization

Edit `app.py` to customize:
- Form fields
- Data validation rules
- Sheet column mappings
- UI styling and layout

## Troubleshooting

### Common Issues

**Error: "No module named 'distutils'"**
- **Solution:** Change `from oauth2 import service_account` to `from google.oauth2 import service_account`

**Error: "Permission denied"**
- **Solution:** Ensure the Google Sheet is shared with your service account email with Editor permissions

**Error: "Spreadsheet not found"**
- **Solution:** Verify the Sheet URL in your secrets configuration is correct

**Error: "Invalid credentials"**
- **Solution:** Check that all fields in `secrets.toml` match your JSON file exactly, especially the `private_key` formatting

### Rate Limiting

Google Sheets API has rate limits. To optimize:
- Use `@st.cache_data` decorator for read operations
- Batch write operations when possible
- Implement exponential backoff for retries

## Security Best Practices

- ✅ Never commit credentials to version control
- ✅ Use Streamlit Cloud's secrets management for production
- ✅ Regularly rotate service account keys
- ✅ Use least-privilege permissions
- ✅ Enable audit logging in Google Cloud Console
- ✅ Restrict Sheet sharing to necessary accounts only

## Dependencies

```
streamlit>=1.50.0
gspread>=6.2.0
google-auth>=2.41.0
google-auth-oauthlib>=1.2.0
pandas>=2.3.0
```

See `requirements.txt` for complete list.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/icu-antibiotic-gs/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/icu-antibiotic-gs/wiki)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Google Sheets integration via [gspread](https://docs.gspread.org/)
- Icons from [Emoji](https://emojipedia.org/)

## Roadmap

- [ ] User authentication and role-based access
- [ ] Advanced analytics and reporting
- [ ] Mobile-responsive design improvements
- [ ] Integration with hospital EMR systems
- [ ] Automated alerts for drug interactions
- [ ] Multi-language support

---

**⚠️ Disclaimer:** This application is for educational and organizational purposes. Always follow your institution's protocols and regulations for medical record keeping and patient data handling.
