from gspread_formatting import format_cell_range, CellFormat, NumberFormat
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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
    row = [today_date, "Allora API", "BTC/USDT", predicted_price, actual_price, round(accuracy, 2)]

    # Append the row
    sheet.append_row(row)
    print("✅ Prediction logged to Google Sheets.")

    # Apply % format to the accuracy cell (last row, column F)
    last_row_index = len(sheet.get_all_values())
    format_cell_range(sheet, f'F{last_row_index}', CellFormat(
        numberFormat=NumberFormat(type='NUMBER', pattern='0.00%')
    ))

def log_prediction_only(predicted_price, block_height):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Allora_Model_Performance_Report").worksheet("Daily Predictions")

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        today,
        "Allora",         
        "BTC/USDT",       
        predicted_price,
        "",               # Placeholder for actual price
        "",               # Placeholder for accuracy
        block_height      # Timestamp or block number
    ])

def update_actual_price(actual_price):
    print("📄 Updating actual price in Google Sheet...")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Allora_Model_Performance_Report").worksheet("Daily Predictions")
    rows = sheet.get_all_values()

    for i, row in enumerate(rows):
        if i == 0:
            continue  # Skip header

        if len(row) < 4:
            print(f" Skipping row {i + 1}: too short")
            continue

        predicted_price_str = row[3]

        if not predicted_price_str:
            print(f" Skipping row {i + 1}: no predicted price")
            continue

        try:
            predicted = float(predicted_price_str)
        except ValueError:
            print(f" Skipping row {i + 1}: invalid predicted price format")
            continue

        if len(row) < 5 or not row[4]:
            # Update actual price and accuracy
            sheet.update_cell(i + 1, 5, actual_price)  # Column E
            accuracy = 100 - abs((predicted - actual_price) / actual_price * 100)
            sheet.update_cell(i + 1, 6, round(accuracy, 2))  # Column F = raw number

            # Format the cell as percentage
            format_cell_range(sheet, f'F{i + 1}', CellFormat(
                numberFormat=NumberFormat(type='NUMBER', pattern='0.00%')
            ))

            print(f"✅ Row {i + 1} updated: Actual={actual_price}, Accuracy={round(accuracy, 2)}%")
        else:
            print(f"ℹ Row {i + 1} already has actual price, skipping")
