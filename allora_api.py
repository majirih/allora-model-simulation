import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_allora_prediction():
    url = "https://allora-api.testnet.allora.network/emissions/v9/latest_network_inferences_outlier_resistant/47"
    headers = {
        "x-api-key": os.getenv("ALLORA_API_KEY")
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Request to Allora API failed: {response.status_code} - {response.text}")
        return None

    data = response.json()
    print("🔍 Raw Allora API response:", data)

    try:
        network_inference = data["network_inferences"]["combined_value"]
        topic_id = data["network_inferences"]["topic_id"]
        block_height = data["inference_block_height"]

        return {
            "prediction": float(network_inference),
            "low": None,  # Not available in this endpoint
            "high": None,
            "topic_id": topic_id,
            "timestamp": block_height
        }
    except KeyError as e:
        print(f"❌ KeyError parsing Allora response: {e}")
        return None
