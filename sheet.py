import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

def append_to_sheet(predicted_price, actual_price, accuracy):
    # Define scope and credentials file
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open spreadsheet and worksheet
    sheet = client.open("Allora_Model_Performance_Report").worksheet("Daily Predictions")

    # Prepare the row
    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [today_date, "Allora API", "BTC/USDT", predicted_price, actual_price, f"{accuracy:.2f}%"]

    # Append the row
    sheet.append_row(row)
    print("✅ Prediction logged to Google Sheets.")
