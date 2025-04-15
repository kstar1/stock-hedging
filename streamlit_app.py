import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import DEFAULT_TICKER
# --- Session State Defaults ---
defaults = {
    "ticker": DEFAULT_TICKER,
    "stock_info": {},
    "selected_expiration": None
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

from src.data.stock_data_provider import get_stock_info, get_historical_price
from src.ui.sidebar import build_sidebar
from src.ui.tabs.put_chain_tab import render_put_chain_tab  # ✅ new import

# --- Page Config ---
st.set_page_config(
    page_title="Stock Hedging Simulator",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Stock Hedging & Option Analysis")

# --- Tab Selector ---
tab_labels = [
    "📊 View Stock Info",
    "📈 PUT Chain Explorer + Breakeven Plot"  # ✅ new tab added
]
active_tab = st.sidebar.radio("🔍 View Mode", tab_labels, key="active_tab")

# --- Sidebar (just ticker) ---
build_sidebar(active_tab)

# --- Fetch Stock Info ---
try:
    st.session_state.stock_info = get_stock_info(st.session_state.ticker)
    current_price = st.session_state.stock_info.get("current_price", 0)
    if not current_price:
        st.error(f"Could not fetch current price for {st.session_state.ticker}.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching stock info: {e}")
    st.stop()

# --- Utility ---
def format_market_cap(value):
    if not isinstance(value, (int, float)):
        return "N/A"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"${value / 1e6:.2f}M"
    else:
        return f"${value:,.0f}"

# === Homepage Tab ===
if active_tab == "📊 View Stock Info":
    info = st.session_state.stock_info

    st.header(f"{st.session_state.ticker} Stock Information")

    if info:
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Current Price",
            f"${current_price:,.2f}",
            f"{current_price - info.get('previous_close', 0):,.2f}"
        )
        col2.metric("Market Cap", format_market_cap(info.get("market_cap")))
        col3.metric("Beta", f"{info.get('beta', 'N/A'):.2f}")

        st.subheader("Recent Price History")
        try:
            hist_data = get_historical_price(st.session_state.ticker, period="1y")
            st.line_chart(hist_data['Close'])
        except Exception as e:
            st.error(f"Could not load historical price chart: {e}")

# === PUT Chain Explorer Tab ===
elif active_tab == "📈 PUT Chain Explorer + Breakeven Plot":
    render_put_chain_tab()
