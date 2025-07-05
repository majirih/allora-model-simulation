# 📄 score_predictions.py
# Fills in actual prices and accuracy for predictions made 24 hours ago

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import requests

# === CONFIGURATION ===
SHEET_NAME = "Allora_Model_Performance_Report"
TAB_NAME = "Daily Predictions"
ASSET = "bitcoin"

# === SETUP GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).worksheet(TAB_NAME)

# === FETCH SHEET DATA ===
data = sheet.get_all_records()
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# === FETCH ACTUAL BTC PRICE ===
def get_actual_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ASSET}&vs_currencies=usd"
    response = requests.get(url)
    price = response.json()[ASSET]["usd"]
    return float(price)

actual_price = get_actual_price()

# === SCAN AND SCORE PREDICTIONS ===
for i, row in enumerate(data):
    row_date = row["Date"]
    if row_date == yesterday and row["Actual Price"] in ("", None):
        predicted = float(row["Predicted Price"])
        accuracy = 100 - abs(actual_price - predicted) / actual_price * 100
        sheet.update_cell(i + 2, 5, actual_price)  # Column E = Actual Price
        sheet.update_cell(i + 2, 6, round(accuracy, 2))  # Column F = Accuracy
        print(f"Updated row {i+2}: Actual = {actual_price}, Accuracy = {round(accuracy, 2)}%")

print("✅ Scoring complete.")
