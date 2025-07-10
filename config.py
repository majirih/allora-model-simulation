import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# GOOGLE SHEETS
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Allora_Model_Performance_Report")
DAILY_SHEET_NAME = os.getenv("DAILY_SHEET_NAME", "Daily Predictions")
SUMMARY_SHEET_NAME = os.getenv("SUMMARY_SHEET_NAME", "Model Performance Summary")

# ALLORA
ALLORA_API_URL = os.getenv("ALLORA_API_URL", "https://api.allora.network")
TOPIC_ID = os.getenv("TOPIC_ID", "4")  # Defaulting to Topic 4 (BTC/USDT 24h)
ALLORA_API_KEY = os.getenv("ALLORA_API_KEY")
