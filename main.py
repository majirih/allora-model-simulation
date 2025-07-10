from sheet import append_to_sheet
from price_fetcher import get_actual_btc_price
from allora_api import fetch_allora_prediction

def run_prediction_workflow():
    print("🚀 Running prediction workflow...")

    # Fetch prediction from Allora
    prediction_data = fetch_allora_prediction()
    print("🧠 Allora Prediction Response:", prediction_data)

    if prediction_data is None:
        print("❌ No prediction received from Allora.")
        return

    predicted_price = prediction_data["prediction"]
    actual_price = get_actual_btc_price()

    accuracy = 100 - abs((predicted_price - actual_price) / actual_price * 100)

    print(f"📈 Predicted: {predicted_price}, Actual: {actual_price}, Accuracy: {accuracy:.2f}%")

    append_to_sheet(predicted_price, actual_price, accuracy)

if __name__ == "__main__":
    run_prediction_workflow()
