"""Test script to verify Google Sheets connection"""
import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1dZhNtCPDG2tAzMkd5FpVh1GqtDXeJFEHhVYd2wY12n0"
SHEET_NAME = "spending-r"
SHEET_RANGE = "A10:O"
CREDENTIALS_FILE = "original-return-107905-3b03bf4c17bf.json"

try:
    print("Authenticating with Google Sheets...")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    print(f"Opening spreadsheet {SPREADSHEET_ID}...")
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    print(f"Reading range {SHEET_RANGE}...")
    data = sheet.get(SHEET_RANGE)

    print(f"✓ Success! Retrieved {len(data)} rows")
    print(f"✓ Headers: {data[0][:5]}...")  # Show first 5 headers
    print(f"✓ Sample row: {data[1][:5]}...")  # Show first 5 columns of first data row

except Exception as e:
    print(f"✗ Error: {e}")
