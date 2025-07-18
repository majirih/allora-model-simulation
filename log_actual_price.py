# log_actual_price.py

from price_fetcher import get_actual_btc_price
from sheet import update_actual_price

def run_actual_logging():
    print("⏱️ Logging actual price after delay...")

    actual_price = get_actual_btc_price()
    if not actual_price:
        print("❌ Failed to fetch actual price.")
        return

    update_actual_price(actual_price)

if __name__ == "__main__":
    run_actual_logging()
