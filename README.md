# 🛡️ TSLA Stock Hedging Simulator

A Python-based command-line tool to help individual investors **hedge their Tesla (TSLA) stock position** using real-time market data from Yahoo Finance.

Built for automation, experimentation, and extension — with clean code modules and logging.

---

## 📈 Features

- ✅ Real-time TSLA stock info and options chain via `yfinance`
- ✅ Filters PUT options based on moneyness, bid-ask spread, and volume
- ✅ Suggests optimal hedge choices using puts
- ✅ Simulates portfolio performance under recession scenarios
- ✅ Visualizes profit/loss for hedged vs unhedged positions
- ✅ Logs simulations to a CSV file for analysis

---

## 🧰 Project Structure

```
stock-hedging/
├── src/
│   ├── config.py               # Local file with number of TSLA shares (excluded from Git)
│   ├── data_fetcher.py         # Pulls TSLA and option chain data
│   ├── option_analyzer.py      # Filters and ranks puts
│   ├── hedge_simulator.py      # Models hedged/unhedged performance
│   ├── visualizer.py           # Plots portfolio profit/loss
│   ├── logger.py               # Logs simulation results to CSV
│   └── main.py                 # CLI entry point
├── logs/
│   └── .gitkeep                # Placeholder (actual logs ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/kstar1/stock-hedging.git
cd stock-hedging

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# (Optional) Add your personal holding in src/config.py
echo "NUM_SHARES = 34.65" > src/config.py
```

---

## 🚀 Run the CLI

```bash
python src/main.py
```

You’ll get a menu to:
- View TSLA stock info
- Explore option chains
- Simulate hedging outcomes
- Plot profit/loss with and without protection

---

## 📝 Sample Output

```
=== Suggested PUT Options ===
contractSymbol  strike  mid_price  volume ...
TSLA240920P00240000  240.0   6.35       1432   ...

✅ Hedge simulation logged successfully.
```

---

## 📊 Sample Plot

_Profit/Loss comparison between unhedged and hedged TSLA portfolio_
*(Insert screenshot later)*

---

## 🔜 TODO / Extensions

- [ ] Export report to PDF or HTML
- [ ] Add CLI flags (e.g. `--simulate`)
- [ ] Streamlit or Flask frontend
- [ ] Integration with multiple tickers (AAPL, NVDA, etc.)

---

## 🤝 Contributing

PRs welcome! Feel free to fork and extend the app.

---
