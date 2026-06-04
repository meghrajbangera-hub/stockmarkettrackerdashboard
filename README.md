# 📈 Nifty 50 + Top 20 Live Tracker

A live stock dashboard tracking all 50 Nifty stocks + 20 top non-Nifty picks.
Built with **Streamlit** + **Yahoo Finance** — free, no API key needed.

## Features

- ✅ Live prices fetched from Yahoo Finance (refreshes every 5 minutes)
- ✅ All 70 stocks — Nifty 50 + Top 20 non-Nifty picks
- ✅ 5-year price charts with indexed comparison
- ✅ Algorithmic buy/hold/watch/sell signals
- ✅ Sector breakdown, gainers vs losers charts
- ✅ Stock deep dive with P/E, 52W high/low, company info
- ✅ Filter by sector, signal, search by name/ticker
- ✅ Dark theme, mobile-friendly

---

## 🚀 Deploy in 3 steps (Free — no credit card)

### Step 1 — Push to GitHub

```bash
# Create a new repo on github.com, then:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/nifty-tracker.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud (free)

1. Go to **share.streamlit.io**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repo → branch: `main` → file: `app.py`
5. Click **Deploy** — done!

Your live URL will be:
```
https://YOUR_USERNAME-nifty-tracker-app-XXXXX.streamlit.app
```

### Step 3 — Share the link

Send the URL to anyone. It's live 24/7 and auto-refreshes every 5 minutes.

---

## 🖥️ Run locally (optional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📊 Data source

All prices are fetched live from **Yahoo Finance** via the `yfinance` library.
- Indian stocks use the `.NS` suffix (NSE)
- Nifty 50 index: `^NSEI`
- Data refreshes every **5 minutes** automatically

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**.
Signals are computed algorithmically from price momentum — not financial advice.
Always consult a SEBI-registered financial advisor before investing.

---

## 🔧 Customise

To add/remove stocks, edit the `TOP20_TICKERS` dictionary in `app.py`:

```python
TOP20_TICKERS = {
    "Your Company Name": "TICKER.NS",  # Add here
    ...
}
```

Find NSE ticker symbols at: [nseindia.com](https://www.nseindia.com)
