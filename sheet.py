import os
import json
import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, CellFormat, NumberFormat
from datetime import datetime, timezone

# ------------------------ GOOGLE SHEETS AUTH ------------------------

def authorize_gspread():
    creds_path = os.environ.get("GOOGLE_CREDS_PATH", "credentials.json")
    creds = Credentials.from_service_account_file(creds_path, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    return gspread.authorize(creds)

# ------------------------ TIMEFRAME TO WORKSHEET NAME ------------------------

def get_worksheet_name(timeframe: str):
    timeframe = timeframe.strip().lower()
    if timeframe == "5-min":
        return "5min Forecast"
    elif timeframe == "8h":
        return "8H Forecast"
    elif timeframe == "24h":
        return "24H Forecast"
    else:
        return None

# ------------------------ UNIFIED PREDICTION LOGGING ------------------------

def log_prediction_only(predicted_price, timestamp, timeframe):
    print("🔧 Starting prediction log...")
    print(f"➡️  Inputs received -> Price: {predicted_price}, Timestamp: {timestamp}, Timeframe: {timeframe}")

    client = authorize_gspread()
    print("✅ Authorized gspread client.")

    worksheet_name = get_worksheet_name(timeframe)
    if not worksheet_name:
        print(f"❌ Unsupported timeframe: {timeframe}")
        return

    print(f"📄 Using worksheet: {worksheet_name}")
    sheet = client.open("Allora_Model_Performance_Report").worksheet(worksheet_name)
    print("✅ Worksheet opened successfully.")

    today = datetime.now().strftime("%Y-%m-%d")
    row = [today, timeframe, "BTC/USDT", predicted_price, "", "", timestamp]
    print(f"📝 Prepared row to append: {row}")

    try:
        sheet.append_row(row)
        all_rows = sheet.get_all_values()
        print(f"📊 Total rows now: {len(all_rows)}")
        print("🧾 Last row in sheet:", all_rows[-1])
        print(f"✅ {timeframe} prediction logged successfully.")
    except Exception as e:
        print(f"❌ Failed to log {timeframe} prediction:", e)

# ------------------------ UNIFIED ACTUAL PRICE UPDATER ------------------------

def update_actual_price(actual_price, target_timestamp_iso, timeframe):
    client = authorize_gspread()

    worksheet_name = get_worksheet_name(timeframe)
    if not worksheet_name:
        print(f"❌ Unsupported timeframe: {timeframe}")
        return False

    sheet = client.open("Allora_Model_Performance_Report").worksheet(worksheet_name)
    data = sheet.get_all_values()

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

                sheet.update_cell(i + 1, 5, actual_price)
                sheet.update_cell(i + 1, 6, round(accuracy, 4))

                # Format accuracy column to percentage
                try:
                    format_cell_range(sheet, f'F{i + 1}', CellFormat(
                        numberFormat=NumberFormat(type='NUMBER', pattern='0.00%')
                    ))
                except Exception as fe:
                    print(f"⚠️ Formatting skipped (not critical): {fe}")

                print(f"✅ Actual + Accuracy updated for row {i+1}: {actual_price}, {round(accuracy, 4)}")
                return True
            except Exception as e:
                print(f"❌ Error updating sheet at row {i+1}: {e}")
                return False

    print("⚠️ No matching row found within ±30s of provided timestamp.")
    return False

# ------------------------ TIMESTAMP SAVER FOR CLOUD ------------------------

def save_timestamp_to_sheet(timeframe, timestamp, predicted_price):
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("Log_Timestamps")
    data = sheet.get_all_values()

    updated = False
    for i in range(1, len(data)):
        if data[i][0].strip().lower() == timeframe.lower():
            sheet.update_cell(i + 1, 2, timestamp)
            sheet.update_cell(i + 1, 3, predicted_price)
            updated = True
            print(f"🔁 Updated timestamp for {timeframe} in Log_Timestamps.")
            break

    if not updated:
        row = [timeframe, timestamp, predicted_price]
        sheet.append_row(row)
        print(f"🆕 Added timestamp for {timeframe} in Log_Timestamps.")

# ------------------------ TIMESTAMP LOADER FROM CLOUD ------------------------

def load_timestamp_from_sheet(timeframe):
    client = authorize_gspread()
    sheet = client.open("Allora_Model_Performance_Report").worksheet("Log_Timestamps")
    data = sheet.get_all_values()

    for i in range(1, len(data)):
        if data[i][0].strip().lower() == timeframe.lower():
            return data[i][1]  # timestamp string

    print(f"⚠️ No saved timestamp for {timeframe} in Log_Timestamps.")
    return None
