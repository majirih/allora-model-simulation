from sheet import update_24h_actual_price, get_last_24h_predicted_row
from price_fetcher import get_actual_btc_price

def run_24h_actual():
    print("🔁 Running 24H actual price logger...")

    # Get last prediction row and predicted price
    row_index, predicted_price = get_last_24h_predicted_row()
    if row_index is None:
        print("❌ No previous 24H prediction found.")
        return

    # Get actual BTC price
    actual_price = get_actual_btc_price()

    # Update actual price and accuracy in Google Sheet
    update_24h_actual_price(actual_price)

    print(f"✅ 24H actual price logged: {actual_price}")

if __name__ == "__main__":
    run_24h_actual()
