# 🛡️ TSLA PUT Option Hedging Simulator

This app helps you simulate the impact of **PUT options** on a portfolio of Tesla (TSLA) shares. It lets you interactively filter options, visualize breakeven zones, and simulate net profit/loss (P&L) outcomes under various hedging strategies.

**Streamlit Version**: [Link](https://stock-hedging-xshbbnr9g3oglugxbujcpn.streamlit.app/)

---

## ⚙️ Features

### 📊 1. View Stock Info
- Displays TSLA stock price, beta, market cap
- Price trend chart (1Y)

### 📉 2. PUT Option Chain Explorer
- Import PUT chain via `yfinance`
- Filter contracts by:
  - Strike range (moneyness)
  - Volume
  - Max # contracts
- Select contracts to **display breakeven zones**
- Interactive Plotly chart:
  - Vertical bars = zones where **capital drops below initial value**
  - Triangle markers = lower or upper breakeven only
  - Hover tooltips for insights

### 💡 3. Simulate Net P&L
- Choose how many contracts to simulate
- Toggle between average purchase price and market price as capital baseline
- Preview **hedge cost**
- Visualize:
  - Red = Loss
  - Green = Profit
- Fully responsive P&L chart

---

## 📁 Project Structure

```bash
├── streamlit_app.py
├── requirements.txt
├── src
│   ├── data
│   │   ├── stock_data_provider.py
│   │   └── option_chain_provider.py
│   ├── sim
│   │   ├── analytics.py
│   │   ├── option_filters.py
│   │   ├── put_breakeven_logic.py
│   │   ├── put_pnl_simulator.py
│   └── ui
│       └── tabs
│           └── put_chain_tab.py
│   └── viz
│       ├── put_breakeven_plot.py
│       └── put_simulation_plot.py
```

---

## 🚀 Getting Started

### Install

```bash
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run streamlit_app.py
```

---

## 🧠 Insights

This tool is ideal for:
- Visual learners who want to explore options risk
- Investors managing drawdowns with limited capital
- Practicing P&L modeling using real-time data

---

## 🧾 Authors

Built by [Kshitij Dutt](https://github.com/kstar1)
with contributions from OpenAI's ChatGPT (logic + UI support).