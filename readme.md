# 🧠 Allora Model Simulation

This project is a simplified, public simulation inspired by [@AlloraNetwork](https://twitter.com/AlloraNetwork). It mimics how decentralized AI models are evaluated, scored, and ranked in real-time using live market data.

### ⚙️ What It Does

- Simulates 3 mock models: `gML_Alpha`, `gML_Beta`, `gML_Gamma`
- Predicts real-time BTC prices around current market value
- Fetches the actual BTC/USD price from CoinGecko
- Calculates prediction accuracy for each model
- Logs everything into a connected Google Sheet
- Auto-updates a `Model Report` leaderboard (average accuracy + win count)

### 📊 How It Works

- `main.py` – the brain of the workflow
- `utils.py` – generates random predictions
- `price_fetcher.py` – gets actual BTC/USD price
- `sheet.py` – connects to and writes to Google Sheets
- `credentials.json` – NOT included (use your own service account key)
- `.gitignore` – excludes sensitive and environment files

### 🧪 Example Output

| Date       | Model       | Asset | Predicted Price | Actual Price | Accuracy |
|------------|-------------|--------|------------------|---------------|----------|
| 2025-07-04 | gML_Alpha   | BTC    | 108221.33        | 107987.22     | 99.78%   |

### 🏆 Leaderboard (Auto-updated)

| Model       | Avg Accuracy (%) | Wins | Total Predictions |
|-------------|------------------|------|--------------------|
| gML_Alpha   | 99.3%            | 3    | 5                  |
| gML_Beta    | 98.7%            | 1    | 5                  |
| gML_Gamma   | 98.9%            | 1    | 5                  |

---

### 🔐 Setup Notes

You’ll need:
- A [Google Cloud service account](https://console.cloud.google.com/)
- Enabled Google Sheets + Drive API
- A `credentials.json` file (excluded from repo)
- Your Google Sheet name & tab pre-set with headers

---

### 🚀 Inspired by Allora

This project was built as a practical demo of Allora’s “self-improving” AI design — with public model evaluation, transparent scoring, and real-time performance logging.

Follow [@AlloraNetwork](https://twitter.com/AlloraNetwork) to understand the future of decentralized intelligence.
