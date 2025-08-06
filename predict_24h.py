from allora_api import fetch_24h_log_return
from sheet import log_prediction_only
from price_fetcher import get_actual_btc_price
import json
from datetime import datetime, timezone

def run_24h_prediction():
    print("🔁 Running 24h prediction (log-return format)...")

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

    # Fallback timestamp if empty
    if not timestamp:
        timestamp = datetime.now(timezone.utc).isoformat()

    print(f"📦 24h predicted absolute price: {predicted_price} at {timestamp}")
    log_prediction_only(predicted_price, timestamp, "24h")

    try:
        with open("last_predicted_24h.json", "w") as f:
            json.dump({"timestamp": timestamp}, f)
    except Exception as e:
        print("⚠️ Could not save timestamp locally:", e)

    print("✅ 24h prediction logged and timestamp saved.")

if __name__ == "__main__":
    run_24h_prediction()
