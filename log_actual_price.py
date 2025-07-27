from price_fetcher import get_actual_btc_price
from sheet import update_actual_price
from datetime import datetime, timedelta, timezone

def run_actual_logging():
    print("⏱️ Logging actual price 5 minutes after prediction...")

    # Get timestamp 5 mins ago and format as ISO without microseconds
    target_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    target_timestamp = target_time.replace(microsecond=0).isoformat()

    actual_price = get_actual_btc_price()
    print(f"📈 Fetched actual price: {actual_price}")

    if not actual_price:
        print("❌ Failed to fetch actual price.")
        return

    try:
        updated = update_actual_price(actual_price, target_timestamp, "5-min")
        if updated:
            print(f"✅ Actual price {actual_price} logged for {target_timestamp}")
        else:
            print(f"⚠️ No match found for prediction at {target_timestamp}")
    except Exception as e:
        print(f"❌ Error logging actual price: {e}")

if __name__ == "__main__":
    run_actual_logging()
