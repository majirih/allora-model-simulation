import requests

def get_actual_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return round(response.json()["bitcoin"]["usd"], 2)
