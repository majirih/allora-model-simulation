import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "python_scripts"))
sys.path.append(os.path.join(os.path.dirname(__file__), "trading_bot"))

from predict_price import run_5min_prediction
from predict_8h import run_8h_prediction
from predict_24h import run_24h_prediction
from trading_bot.trade_bot import run_trade_bot

def main():
    parser = argparse.ArgumentParser(description="Allora Forecast & Trade Bot")
    parser.add_argument("--run-5min", action="store_true", help="Run 5-min prediction")
    parser.add_argument("--run-8h", action="store_true", help="Run 8h prediction")
    parser.add_argument("--run-24h", action="store_true", help="Run 24h prediction")
    parser.add_argument("--run-trade", action="store_true", help="Run trading logic")

    args = parser.parse_args()

    if args.run_5min:
        print("🟢 5-min flag received")
        run_5min_prediction()

    if args.run_8h:
        print("🟢 8h flag received")
        run_8h_prediction()

    if args.run_24h:
        print("🟢 24h flag received")
        run_24h_prediction()

    if args.run_trade:
        print("🤖 Running trading bot...")
        run_trade_bot()

if __name__ == "__main__":
    main()
