import requests
from sheet import update_8h_actual_price

def fetch_actual_btc_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={
            "ids": "bitcoin",
            "vs_currencies": "usd"
        })

        data = response.json()
        actual_price = data["bitcoin"]["usd"]
        print(f"📈 Fetched actual BTC price: ${actual_price}")
        return actual_price

    except Exception as e:
        print("❌ Error fetching actual BTC price:", e)
        return None

def main():
    actual_price = fetch_actual_btc_price()
    if actual_price is not None:
        update_8h_actual_price(actual_price)

if __name__ == "__main__":
    main()
