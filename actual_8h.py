from price_fetcher import get_actual_btc_price
from sheet import update_actual_price
from datetime import datetime, timezone
import json

def run_actual_logging():
    print("⏱️ Logging actual price 8 hours after prediction...")

    try:
        with open("last_predicted_8h.json", "r") as f:
            timestamp = json.load(f)["timestamp"]
    except Exception as e:
        print("❌ Could not load 8h timestamp:", e)
        return

    actual_price = get_actual_btc_price()
    print(f"📈 Fetched actual price: {actual_price}")

    if not actual_price:
        print("❌ Failed to fetch actual price.")
        return

    try:
        updated = update_actual_price(actual_price, timestamp, "8H")
        if updated:
            print(f"✅ Actual price {actual_price} logged for {timestamp}")
        else:
            print(f"⚠️ No matching row for prediction at {timestamp}")
    except Exception as e:
        print(f"❌ Error updating actual price: {e}")

if __name__ == "__main__":
    run_actual_logging()
