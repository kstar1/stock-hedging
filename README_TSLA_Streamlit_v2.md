# 🛡️ TSLA Hedging Simulator (Streamlit v2)

This is an educational tool to visualize the financial impact of protective PUT options on your Tesla (TSLA) stock holdings. The app uses real-time market data and simulates how PUT contracts can hedge your downside risk.

---

## 🚀 Features (v2 Streamlit Branch)

- 📊 **View Stock Info** – See TSLA's current price, market cap, and 1-year chart
- 📈 **PUT Chain Explorer** – Visualize breakeven zones for available PUT contracts
- 💸 **Strike-based Contract Selection** – Select contracts using human-readable strike price
- 🧠 **Breakeven Explanation** – Learn when you'd regain your initial capital if TSLA rises or falls
- 🎨 **Volume-Colored Breakeven Plot** – Visual display of hedging zones, color-coded by option volume

---

## ▶️ How to Run the App

### 🖥️ MacOS/Linux (Terminal)
```bash
# 1. Clone the repo if you haven't
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

### 🪟 Windows (PowerShell or CMD)
```bash
# 1. Clone the repo if you haven't
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

---

## 🧩 File Structure

```plaintext
├── streamlit_app.py
├── config/
│   └── settings.py
├── src/
│   ├── data/
│   │   └── option_chain_provider.py
│   ├── sim/
│   │   ├── analytics.py
│   │   └── option_filters.py
│   ├── ui/
│   │   ├── sidebar.py
│   │   └── tabs/
│   │       └── put_chain_tab.py
│   └── viz/
│       └── option_charts.py
```

---

## 📎 Notes

- Data is fetched via `yfinance` (no API key required)
- Each PUT contract assumes 100-share lot size
- No transaction costs, taxes, or slippage modeled (yet)

---

## 🤝 Contributing

Want to add CALL option support or build the Hedge Simulator tab? Fork and PR welcome!

---

Built with 💙 by [YOUR NAME]