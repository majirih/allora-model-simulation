import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, CellFormat, NumberFormat
from datetime import datetime, timezone

# ------------------------ GOOGLE SHEETS AUTH ------------------------

def authorize_gspread():
    creds = Credentials.from_service_account_file("credentials.json", scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    return gspread.authorize(creds)

# ------------------------ 5-MIN FORECAST FUNCTIONS ------------------------

def log_prediction_only(predicted_price, timestamp, timeframe):
    """Log prediction to the appropriate worksheet based on timeframe."""
    print("🔧 Starting prediction log...")
    print(f"➡️  Inputs received -> Price: {predicted_price}, Timestamp: {timestamp}, Timeframe: {timeframe}")

    client = authorize_gspread()
    print("✅ Authorized gspread client.")

    if timeframe == "5-min":
        worksheet_name = "5min Forecast"
    elif timeframe == "8H":
        worksheet_name = "8H Forecast"
    elif timeframe == "24H":
        worksheet_name = "24H Forecast"
    else:
        print("❌ Unsupported timeframe:", timeframe)
        return

    print(f"📄 Using worksheet: {worksheet_name}")
    sheet = client.open("Allora_Model_Performance_Report").worksheet(worksheet_name)
    print("✅ Worksheet opened successfully.")
    
    now = datetime.now().strftime("%Y-%m-%d")
    row = [now, timeframe, "BTC/USDT", predicted_price, "", "", timestamp]
    print(f"📝 Prepared row to append: {row}")

    try:
        sheet.append_row(row)
        all_rows = sheet.get_all_values()
        print(f"📊 Total rows now: {len(all_rows)}")
        print("🧾 Last row in sheet:", all_rows[-1])
        print(f"✅ {timeframe} prediction logged successfully.")
    except Exception as e:
        print(f"❌ Failed to log {timeframe} prediction:", e)

def update_actual_price(actual_price, target_timestamp_iso):
    """Update 5-min actual price and compute accuracy based on approximate timestamp match."""
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("5min Forecast")
    data = sheet.get_all_values()

    # Parse ISO target timestamp into datetime, then convert to UNIX
    try:
        target_dt = datetime.fromisoformat(target_timestamp_iso)
    except ValueError:
        print("❌ Invalid target timestamp format.")
        return False

    target_unix = int(target_dt.replace(tzinfo=timezone.utc).timestamp())

    for i in range(1, len(data)):
        row = data[i]
        if len(row) < 7:
            continue

        sheet_ts_str = row[6].strip()
        actual_col = row[4].strip()

        try:
            # Handle both ISO and UNIX strings in the sheet
            if "T" in sheet_ts_str:
                sheet_dt = datetime.fromisoformat(sheet_ts_str)
                sheet_unix = int(sheet_dt.replace(tzinfo=timezone.utc).timestamp())
            else:
                sheet_unix = int(float(sheet_ts_str))
        except Exception as e:
            print(f"⛔️ Skipping row {i+1} due to timestamp parse error: {e}")
            continue

        if abs(sheet_unix - target_unix) <= 30 and actual_col == "":
            try:
                predicted_price = float(row[3])
                accuracy = 1 - abs(predicted_price - actual_price) / actual_price

                sheet.update_cell(i + 1, 5, actual_price)          # Column E: Actual Price
                sheet.update_cell(i + 1, 6, round(accuracy, 4))    # Column F: Accuracy

                format_cell_range(sheet, f'F{i + 1}', CellFormat(
                    numberFormat=NumberFormat(type='NUMBER', pattern='0.00%')
                ))

                print(f"✅ Actual + Accuracy updated for row {i+1}: {actual_price}, {round(accuracy, 4)}")
                return True
            except Exception as e:
                print(f"❌ Error updating sheet at row {i+1}: {e}")
                return False

    print("⚠️ No matching row found within ±30s of provided timestamp.")
    return False
# ------------------------ 24H FORECAST FUNCTIONS ------------------------

def log_24h_prediction_only(predicted_price, timestamp):
    """Log 24H prediction to Google Sheets."""
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("24H Forecast")

    now = datetime.now().strftime("%Y-%m-%d")
    row = [now, "24H", "BTC/USDT", predicted_price, "", "", timestamp]
    print("🧪 Prepared row for Google Sheets:", row)
    print("📄 Target worksheet: 24H Forecast")

    try:
        sheet.append_row(row)
        print("✅ 24H prediction logged.")
    except Exception as e:
        print("❌ Failed to log 24H prediction:", e)

def update_24h_actual_price(actual_price):
    """Update 24H actual price and compute accuracy."""
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("24H Forecast")
    data = sheet.get_all_values()

    for i in reversed(range(1, len(data))):
        if data[i][4] == "":  # E column (Actual Price) is empty
            try:
                predicted_price = float(data[i][3])  # D column
                accuracy = 1 - abs(predicted_price - actual_price) / actual_price

                sheet.update_cell(i + 1, 5, actual_price)          # E column
                sheet.update_cell(i + 1, 6, round(accuracy, 4))    # F column

                format_cell_range(sheet, f'F{i + 1}', CellFormat(
                    numberFormat=NumberFormat(type='NUMBER', pattern='0.00%')
                ))

                print("✅ 24H actual price + accuracy updated:", actual_price, round(accuracy, 4))
                return
            except Exception as e:
                print("❌ Error updating 24H actual price:", e)
                return

def get_last_24h_predicted_row():
    """Fetch the last logged 24H prediction row that hasn't been updated with an actual price yet."""
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("24H Forecast")
    data = sheet.get_all_values()

    for i in reversed(range(1, len(data))):
        if data[i][4] == "":  # Column E is empty (Actual Price)
            try:
                row_index = i + 1  # Adjust for 0-index
                predicted_price = float(data[i][3])  # Column D (Predicted Price)
                return row_index, predicted_price
            except Exception as e:
                print("❌ Error reading 24H predicted price:", e)
                return None, None

    print("⚠️ No pending 24H prediction found.")
    return None, None

# ------------------------ 8H FORECAST FUNCTIONS ------------------------

def log_8h_prediction_only(predicted_price, timestamp):
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("8H Forecast")

    now = datetime.now().strftime("%Y-%m-%d")
    row = [now, "8H", "BTC/USDT", predicted_price, "", "", timestamp]
    print("🧪 Prepared row for Google Sheets:", row)
    print("📄 Target worksheet: 8H Forecast")

    try:
        sheet.append_row(row)
        print("✅ 8H prediction logged.")
    except Exception as e:
        print("❌ Failed to log 8H prediction:", e)

# === NEW: 8H Actual Price Updater ===
def update_8h_actual_price(actual_price):
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("8H Forecast")
    data = sheet.get_all_values()

    for i in reversed(range(len(data))):
        if data[i][4] == "":
            predicted = float(data[i][3])
            actual = float(actual_price)
            accuracy = round((1 - abs(predicted - actual) / actual) * 100, 2)
            sheet.update_cell(i + 1, 5, actual_price)
            sheet.update_cell(i + 1, 6, f"{accuracy}%")
            print(f"✅ Updated 8H actual price for row {i + 1}")
            break

# === Optional: Fetch Last 8H Row for Debugging ===
def get_last_8h_predicted_row():
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("8H Forecast")
    data = sheet.get_all_values()

    for row in reversed(data):
        if row[4] == "":
            return row
    return None
