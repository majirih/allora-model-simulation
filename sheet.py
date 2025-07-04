import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def append_to_sheet(model_predictions, actual_price, model_accuracies, asset="BTC"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Allora_Model_Performance_Report").worksheet("Daily Predictions")

    date_str = datetime.now().strftime("%Y-%m-%d")

    for model in model_predictions:
        row = [
            date_str,
            model,
            asset,
            model_predictions[model],
            actual_price,
            model_accuracies[model]
        ]
        sheet.append_row(row)