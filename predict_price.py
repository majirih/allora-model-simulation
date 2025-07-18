# predict_price.py

from allora_api import fetch_allora_prediction
from price_fetcher import get_actual_btc_price
from sheet import log_prediction_only

def run_prediction():
    print(" Running prediction logging...")

    prediction = fetch_allora_prediction()
    if not prediction:
        print(" No prediction received from Allora.")
        return

    predicted_price = prediction["prediction"]
    timestamp = prediction["timestamp"]

    print(f" Logged Predicted: {predicted_price} at block {timestamp}")
    log_prediction_only(predicted_price, timestamp)

if __name__ == "__main__":
    run_prediction()
