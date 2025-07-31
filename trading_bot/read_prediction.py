import os
import json
import gspread

from google.oauth2.service_account import Credentials

def get_latest_5min_prediction(sheet_name='Allora_Model_Performance_Report', worksheet_name='5min Forecast'):

    scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
    google_creds = json.loads(os.environ.get("GOOGLE_CREDS_JSON"))
    creds = Credentials.from_service_account_info(google_creds, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)

    worksheet = sheet.worksheet(worksheet_name)

    rows = worksheet.get_all_records()

    if not rows:
        print("No data found in sheet.")
        return None
    
    latest = rows[-1]

    return {
        "timestamp": latest['Date'],
        "predicted_price": float(latest['Predicted Price']),
        "actual_price": float(latest['Actual Price']) if latest['Actual Price'] else None
    }

if __name__ == "__main__":
    latest = get_latest_5min_prediction()
    print("Latest Prediction:", latest)
