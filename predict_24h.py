from allora_api import fetch_24h_log_return
from sheet import log_prediction_only
from price_fetcher import get_actual_btc_price
import json

def run_prediction():
    print("🔁 Running 24h prediction (log-return format)...")

    # Get current BTC price (needed to convert log-return to absolute price)
    current_price = get_actual_btc_price()
    if not current_price:
        print("❌ Failed to fetch current BTC price.")
        return

    prediction = fetch_24h_log_return(current_price)
    if not prediction:
        print("❌ No 24h prediction received from Allora.")
        return

    predicted_price = prediction["predicted_price"]
    timestamp = prediction["timestamp"]

    print(f"📦 24h predicted absolute price: {predicted_price} at {timestamp}")
    log_prediction_only(predicted_price, timestamp, "24h")

    # Save timestamp for actual logger
    with open("last_predicted_24h.json", "w") as f:
        json.dump({"timestamp": timestamp}, f)

    print("✅ 24h prediction logged and timestamp saved.")

if __name__ == "__main__":
    run_prediction()
