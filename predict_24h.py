from allora_api import fetch_24h_log_return
from price_fetcher import get_actual_btc_price
from sheet import log_24h_prediction_only
import math
from datetime import datetime, timezone

def run_24h_prediction():
    print("📈 Running 24H prediction logging...")

    # Get current BTC price
    btc_price = get_actual_btc_price()
    if not btc_price:
        print("❌ Failed to fetch current BTC price.")
        return

    # Get forecast (requires current price)
    forecast = fetch_24h_log_return(btc_price)
    if not forecast:
        print("❌ No forecast received.")
        return

    # Convert ISO 8601 timestamp string to UTC datetime
    dt_object = datetime.fromisoformat(forecast["timestamp"].replace("Z", "+00:00"))

    # Convert log-return to absolute price
    predicted_price = btc_price * math.exp(forecast["log_return"])

    # Log to Google Sheet — only passing predicted_price and timestamp now
    try:
        log_24h_prediction_only(round(predicted_price, 2), forecast["timestamp"])
        print("✅ Logged 24H prediction:", round(predicted_price, 2), forecast["timestamp"])
    except Exception as e:
        print(f"❌ Failed to log 24H prediction: {e}")

if __name__ == "__main__":
    run_24h_prediction()
