# TSLA Stock Hedging Toolkit

This CLI-based application helps individual investors evaluate and simulate hedging strategies using put options for TSLA stock.

## 🔧 Features

### 1. View Stock and Option Data
- Pulls real-time TSLA stock data via `yfinance`
- Lists available PUT option expiration dates and filtered contracts
- Saves raw and filtered chains for inspection

### 2. Simulate Hedging Scenarios
- Plot P&L for unhedged vs. put-hedged portfolio
- Visualize breakeven zones for each PUT option
- Identify effective hedging contracts based on strike, premium, volume, and breakeven logic

### 3. Portfolio Decision Support
- Simulate capital-preserving hedge based on your budget and funding method (cash/sell shares)
- Compute ROI on hedging
- Shade profit/loss zones in plots

### 4. Logging & Insights
- Logs all simulations with input/output data for audit and future analysis
- Explains graph regions and breakeven logic clearly in terminal output

---

## 💻 How to Use

```bash
# Install dependencies (recommended to use Python 3.10 or 3.11)
pip install -r requirements.txt

# Run the app
python src/main.py
```

The app will prompt you to select options interactively.

---

## 🧠 Example Scenario

You hold 34.65 shares of TSLA bought at $429. You're worried about a downturn and want to explore protective puts.

- Use Option 5 to filter contracts by volume, price, and strike
- See breakeven zones graphically
- Simulate payoff for any contract

---

## 📂 Project Structure

```
src/
├── main.py                  # Entry point
├── data_fetcher.py          # Loads stock + options data
├── hedge_simulator.py       # Option 5 simulations
├── hedge_decision_simulator.py  # Option 6 logic
├── visualizer.py            # All matplotlib plots
├── utils.py                 # Helpers for calculations
├── logger.py                # Logging all scenarios
├── config/                  # Filter config
└── logs/                    # Output logs and breakeven CSVs
```

---

## 🧾 Notes
- Currently supports **TSLA** but can be extended to other tickers
- All data sourced from Yahoo Finance (via `yfinance`)
- Volume-based color gradation for strike selection visualization

---

## 🧠 Future Features
- Toggle filters (IV/volume/etc.)
- Combine web scraping to infer sentiment
- Optimal hedge contract selector
- Multi-leg hedge strategies (coming soon!)

---

## ⚠️ Known Limitations
- Number of PUT contracts shown may be filtered due to the current volume/strike range config. Modify `config_filters.py` to widen this.
- Some features rely on clean NumPy/Pandas compatibility. Avoid NumPy 2.x for now if issues occur.

---

Developed by [Kshitij Dutt](https://github.com/kstar1) as a hands-on investing assistant.