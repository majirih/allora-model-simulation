from allora_api import fetch_8h_prediction
from sheet import log_prediction_only
import json
from datetime import datetime

def run_prediction():
    print("🔁 Running 8h prediction logging...")

    prediction = fetch_8h_prediction()
    if not prediction:
        print("❌ No 8h prediction received from Allora.")
        return

    print("📦 Raw 8h prediction:", prediction)

    predicted_price = prediction["predicted_price"]

    # ✅ Use current UTC timestamp since Allora doesn’t return it
    timestamp = datetime.utcnow().isoformat()

    print(f"✅ Logged 8h Predicted: {predicted_price} at {timestamp}")
    log_prediction_only(predicted_price, timestamp, "8h")

    # ✅ Save timestamp to file so actual logger can match it later
    with open("last_predicted_8h.json", "w") as f:
        json.dump({"timestamp": timestamp}, f)

if __name__ == "__main__":
    run_prediction()
