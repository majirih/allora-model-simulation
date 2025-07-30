import os
import json
from datetime import datetime

# ✅ Direct imports assuming this file is in /trading_bot/
from price_fetcher import get_actual_btc_price
from read_prediction import get_latest_5min_prediction

# File paths (relative to project root)
WALLET_PATH = os.path.join("data", "wallet.json")
TRADE_LOG_PATH = os.path.join("data", "trade_log.csv")

# Config
TRADE_AMOUNT_USDT = 100  # Fixed amount to buy/sell
THRESHOLD = 0.01         # 1% difference to trigger trade

# Load wallet
def load_wallet():
    with open(WALLET_PATH, 'r') as f:
        return json.load(f)

# Save wallet
def save_wallet(wallet):
    with open(WALLET_PATH, 'w') as f:
        json.dump(wallet, f, indent=4)

# Log trade to CSV
def log_trade(action, predicted, actual, amount, pnl, reason):
    row = f"{datetime.utcnow()},{action},{predicted},{actual},{amount},{pnl},{reason}\n"
    try:
        with open(TRADE_LOG_PATH, 'a') as f:
            f.write(row)
    except FileNotFoundError:
        with open(TRADE_LOG_PATH, 'w') as f:
            f.write("timestamp,action,predicted_price,actual_price,amount,PnL,reason\n")
            f.write(row)

# Core trading logic
def run_trade_bot():
    print("🤖 Running trading agent...")

    wallet = load_wallet()

    prediction = get_latest_5min_prediction()
    if not prediction:
        print("❌ No prediction found.")
        return

    predicted_price = prediction["predicted_price"]
    current_price = get_actual_btc_price()

    if not current_price:
        print("❌ Failed to fetch live BTC price.")
        return

    print(f"🔍 Predicted: {predicted_price} | Actual: {current_price}")
    price_diff_pct = (predicted_price - current_price) / current_price

    if price_diff_pct >= THRESHOLD:
        if wallet["USDT"] >= TRADE_AMOUNT_USDT:
            btc_bought = TRADE_AMOUNT_USDT / current_price
            wallet["USDT"] -= TRADE_AMOUNT_USDT
            wallet["BTC"] += btc_bought
            log_trade("BUY", predicted_price, current_price, TRADE_AMOUNT_USDT, "-", "Prediction > Market (BUY)")
            print(f"✅ Bought ${TRADE_AMOUNT_USDT} worth of BTC at {current_price}")
        else:
            print("⚠️ Not enough USDT to buy.")

    elif price_diff_pct <= -THRESHOLD:
        btc_to_sell = TRADE_AMOUNT_USDT / current_price
        if wallet["BTC"] >= btc_to_sell:
            wallet["BTC"] -= btc_to_sell
            wallet["USDT"] += TRADE_AMOUNT_USDT
            log_trade("SELL", predicted_price, current_price, TRADE_AMOUNT_USDT, "-", "Prediction < Market (SELL)")
            print(f"✅ Sold {btc_to_sell:.6f} BTC for ${TRADE_AMOUNT_USDT}")
        else:
            print("⚠️ Not enough BTC to sell.")

    else:
        print("⏸ No significant difference — HOLD")

    save_wallet(wallet)

# Allow manual testing
if __name__ == "__main__":
    run_trade_bot()
