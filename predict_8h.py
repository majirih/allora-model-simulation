# predict_8h.py

from allora_api import fetch_8h_prediction
from sheet import log_8h_prediction_only
from datetime import datetime

def run_8h_prediction():
    print("📈 Running 8H prediction logging...")

    prediction = fetch_8h_prediction()
    if not prediction:
        print("❌ Failed to fetch 8H prediction.")
        return

    predicted_price = prediction["predicted_price"]
    timestamp = datetime.now().isoformat()

    log_row = [datetime.now().strftime("%Y-%m-%d"), "8H", "BTC/USDT", predicted_price, "", "", f'{prediction["block_height"]} / {timestamp}']
    
    try:
        log_8h_prediction_only(predicted_price, timestamp)
        print("✅ Logged 8H prediction:", log_row)
    except Exception as e:
        print("❌ Failed to log 8H prediction:", e)

if __name__ == "__main__":
    run_8h_prediction()
