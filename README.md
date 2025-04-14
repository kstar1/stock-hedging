# TSLA Hedging & Option Analysis App

This project helps investors simulate and visualize option-based hedging strategies — especially protective PUTs — for TSLA and other tickers. It is transitioning from a CLI tool into an interactive **Streamlit web app**.

## 🚀 Features (CLI & Streamlit MVP)

### ✅ Current (CLI)
- TSLA stock data and historical price chart
- PUT option chain fetcher (from Yahoo Finance)
- Filter by volume, strike proximity, bid-ask spread
- Simulate payoff of buying a PUT (Option 5)
- Simulate capital-preserving hedge (Option 6)
- Breakeven zone plot with color-coded volume
- All results logged and saved

### 🧱 Streamlit App In Progress
- Interactive dashboard to:
  - Input #shares, purchase price, hedge budget
  - Choose expiration and PUT contracts
  - Simulate P&L visually
  - Generate insights and breakeven maps
- Download session logs and contract summaries
- Support for **any ticker**, not just TSLA
- Extendable to **CALL options** and multi-leg strategies

## 📂 Folder Structure (Recommended)

```
stock-hedging/
├── src/
│   ├── cli/ (optional legacy)
│   ├── sim/
│   ├── viz/
│   ├── data/
│   ├── utils/
├── config/
├── logs/
├── streamlit_app.py  👈 main app file
├── requirements.txt
└── README.md
```

## 🧠 Future Capabilities
- Call option simulation
- AI-powered summaries of option chains
- Multi-leg strategy simulation (spreads, collars)
- Dynamic filters (IV, volume, moneyness sliders)
- Sentiment signals from web/news
- Optimal contract ranking engine

## 📦 Setup

```bash
# Set up venv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

---

Built by [Kshitij Dutt](https://github.com/kstar1) — designed to make retail hedging simple, smart, and data-backed.