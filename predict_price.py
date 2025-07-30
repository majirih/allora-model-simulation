from allora_api import fetch_5min_prediction
from sheet import log_prediction_only

def run_5min_prediction():
    print("🔁 Running 5-min prediction logging...")

    prediction = fetch_5min_prediction()
    if not prediction:
        print("❌ No prediction received from Allora.")
        return

    print("📦 Raw prediction response:", prediction)

    predicted_price = prediction["predicted_price"]
    timestamp = prediction["timestamp"]

    print(f"✅ Logged Predicted: {predicted_price} at block {timestamp}")
    log_prediction_only(predicted_price, timestamp, "5-min")

if __name__ == "__main__":
    run_5min_prediction()
