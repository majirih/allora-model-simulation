import os
import math
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://allora-api.testnet.allora.network/emissions/v9/latest_network_inferences_outlier_resistant"

# ✅ Topic 47 — BTC/USDT 5-min price forecast
def fetch_5min_prediction():
    topic_id = 47
    url = f"{BASE_URL}/{topic_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result = data["network_inferences"]
        predicted_price = float(result["combined_value"])
        block_height = int(data["inference_block_height"])
        timestamp = datetime.utcnow().isoformat()

        return {
            "predicted_price": predicted_price,
            "block_height": block_height,
            "topic_id": topic_id,
            "timestamp": timestamp
        }

    except Exception as e:
        print(f"❌ Error fetching 5-min prediction (Topic {topic_id}):", e)
        return None


# ✅ Topic 61 — BTC/USDT 24h log-return forecast
def fetch_24h_log_return(current_price):
    topic_id = 61
    url = f"{BASE_URL}/{topic_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result = data["network_inferences"]
        log_return = float(result["combined_value"])
        block_height = int(data["inference_block_height"])
        predicted_price = current_price * math.exp(log_return)
        timestamp = datetime.utcnow().isoformat()

        return {
            "log_return": log_return,
            "predicted_price": predicted_price,
            "block_height": block_height,
            "topic_id": topic_id,
            "current_price": current_price,
            "timestamp": timestamp
        }

    except Exception as e:
        print(f"❌ Error fetching 24h log-return prediction (Topic {topic_id}):", e)
        return None
    
# ✅ Topic 42 — BTC/USDT 8h log-return forecast
def fetch_8h_prediction():
    """Fetch 8-hour BTC/USDT price prediction from Allora Topic 42."""
    topic_id = 42  # 8-hour BTC/USDT forecast
    url = f"{BASE_URL}/{topic_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        combined_value = float(data["network_inferences"]["combined_value"])
        block_height = int(data["inference_block_height"])
        timestamp = data.get("inference_timestamp", "")  # Optional, some topics include this

        return {
            "predicted_price": combined_value,
            "block_height": block_height,
            "timestamp": timestamp,
            "topic_id": topic_id
        }
    except Exception as e:
        print(f"❌ Error fetching 8H prediction from Topic {topic_id}:", e)
        return None