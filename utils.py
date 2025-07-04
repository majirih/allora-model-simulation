import random

MODELS = ["gML_Alpha", "gML_Beta", "gML_Gamma"]

def get_prediction_data(base_price=108000):
    predictions = {}
    for model in MODELS:
        fluctuation = random.uniform(-400, 400)  # Wider range for high price
        predictions[model] = round(base_price + fluctuation, 2)
    return predictions