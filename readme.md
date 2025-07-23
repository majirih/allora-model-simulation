# 📊 Allora Live Prediction Dashboard

A real-time dashboard that displays predictions from the [Allora Network](https://allora.network), now supporting **multiple timeframes**:

- **5-minute forecast** (Topic 47)  
- **8-hour forecast** (Topic 42)  
- **24-hour forecast** (Topic 61)

> This project fetches on-chain inference results from Allora's testnet API, logs them into Google Sheets, and displays them via a Next.js frontend deployed on Vercel.

---

## 🧰 Tech Stack

- **Allora API** — Source of real-time BTC/USDT predictions  
- **Google Sheets** — Stores predicted and actual prices for 5min, 8H, and 24H timeframes  
- **Next.js + React** — Dashboard frontend  
- **Vercel** — Hosting and continuous deployment  
- **Python** — Backend logging script with Task Scheduler for automation  

---

## 🚀 Key Features

- **Multi-Timeframe Dashboard**  
  View predictions for:
  - **5min** (Topic 47)
  - **8H** (Topic 42)
  - **24H** (Topic 61, log-return converted to absolute price)

- **Live Forecast Display**
  - Predicted Price  
  - Actual Price (via CoinGecko)  
  - Accuracy %  
  - Timestamp  
  - Block Height  

- **Auto-Refreshing Data**  
  - Pulls data from Google Sheets on page load  
  - Dynamic switching via query param:  
    `?timeframe=5min` / `8H` / `24H`

- **Secure API Key Management**  
  - Environment variables via `.env.local` and Vercel dashboard  

---

## 🌐 Live Deployment

- **Frontend**: [allora-dashboard.vercel.app](https://allora-dashboard.vercel.app)  
- **Codebase**: [GitHub Repo](https://github.com/majirih/allora-dashboard)

---

## 🔌 Allora API Endpoints

- **5min (Topic 47)**  
```bash
https://allora-api.testnet.allora.network/emissions/v9/latest_network_inferences_outlier_resistant/47
