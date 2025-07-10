# 📊 Allora Live Prediction Dashboard

A real-time dashboard that displays predictions from the [Allora Network](https://allora.network), focusing on **Topic 47: BTC/USDT 5-minute prediction**.

> This project fetches on-chain inference results from Allora's testnet API, logs them into Google Sheets, and displays them via a Next.js frontend deployed on Vercel.

---

##  Tech Stack

- **Allora API** — Source of real-time BTC/USDT predictions  
- **Google Sheets** — Stores predicted and actual prices  
- **Next.js + React** — Dashboard frontend  
- **Vercel** — Hosting and continuous deployment  
- **Python** — Backend logger that runs periodically via Task Scheduler  

---

## Key Features

- **Live Dashboard** — Displays most recent prediction with:
  - Predicted Price
  - Actual Price (from CoinGecko)
  - Accuracy %
  - Prediction Timestamp

- **Auto-Refreshing Data** — Pulls data from Google Sheets on load  
- **Secure API Key Handling** — via `.env.local` and Vercel Secrets  

---

## Live Project

- **Frontend**: [allora-dashboard.vercel.app](https://allora-dashboard.vercel.app)  
- **Code**: [GitHub Repository](https://github.com/majirih/allora-dashboard)

---

## Prediction Source

```bash
https://allora-api.testnet.allora.network/emissions/v9/latest_network_inferences_outlier_resistant/47
