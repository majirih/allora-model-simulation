# log_actual_price.py

from price_fetcher import get_actual_btc_price
from sheet import update_actual_price

def run_actual_logging():
    print("⏱️ Logging actual price after delay...")

    actual_price = get_actual_btc_price()
    print(f"📈 Fetched actual price: {actual_price}")

    if not actual_price:
        print("❌ Failed to fetch actual price.")
        return

    try:
        updated = update_actual_price(actual_price)  # <-- Add timeframe label
        if updated:
            print(f"✅ Actual price {actual_price} logged successfully.")
        else:
            print("⚠️ No matching row found to log actual price. Prediction might not exist or was already filled.")
    except Exception as e:
        print(f"❌ Error updating 5-min actual price: {e}")

if __name__ == "__main__":
    run_actual_logging()
