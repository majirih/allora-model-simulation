import os
import json
import gspread

def get_latest_5min_prediction(sheet_name='Allora_Model_Performance_Report', worksheet_name='5min Forecast'):

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    google_creds = json.loads(os.environ.get("GOOGLE_CREDS_JSON"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
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
