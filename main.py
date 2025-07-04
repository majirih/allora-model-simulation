from utils import get_prediction_data
from sheet import append_to_sheet
from price_fetcher import get_actual_btc_price

def calculate_accuracy(predicted, actual):
    return round((1 - abs(predicted - actual) / actual) * 100, 2)

def run_prediction_workflow():
    print("Running prediction workflow...")

    actual_price = get_actual_btc_price()
    print(f"📈 Actual BTC Price: ${actual_price}")

    model_predictions = get_prediction_data(base_price=actual_price)
    print("🧠 Predictions:", model_predictions)

    model_accuracies = {
        model: calculate_accuracy(pred, actual_price)
        for model, pred in model_predictions.items()
    }

    append_to_sheet(model_predictions, actual_price, model_accuracies)

if __name__ == "__main__":
    run_prediction_workflow()
