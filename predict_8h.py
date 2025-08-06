from allora_api import fetch_8h_prediction
from sheet import log_prediction_only
import json
from datetime import datetime, timezone

def run_8h_prediction():
    print("🔁 Running 8h prediction logging...")

    prediction = fetch_8h_prediction()
    if not prediction:
        print("❌ No 8h prediction received from Allora.")
        return

    print("📦 Raw 8h prediction:", prediction)

    predicted_price = prediction["predicted_price"]
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"✅ Logged 8h Predicted: {predicted_price} at {timestamp}")
    log_prediction_only(predicted_price, timestamp, "8h")

    # Save timestamp to file (for local use only)
    try:
        with open("last_predicted_8h.json", "w") as f:
            json.dump({"timestamp": timestamp}, f)
    except Exception as e:
        print("⚠️ Could not save timestamp locally:", e)

if __name__ == "__main__":
    run_8h_prediction()
