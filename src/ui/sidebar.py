import streamlit as st
from config.settings import DEFAULT_TICKER

def build_sidebar(active_tab: str):
    st.sidebar.title("⚙️ Configuration")

    # Always show Ticker input
    st.session_state.ticker = st.sidebar.text_input(
        "Ticker Symbol", 
        value=st.session_state.get("ticker", DEFAULT_TICKER)
    ).upper()

    if active_tab != "📊 View Stock Info":
        st.sidebar.markdown("---")
        st.sidebar.header("📊 Portfolio Input")
        st.session_state.shares = st.sidebar.number_input(
            "Number of Shares",
            min_value=0.0,
            value=st.session_state.get("shares", 34.65),
            step=1.0
        )
        st.session_state.avg_price = st.sidebar.number_input(
            "Average Purchase Price ($)",
            min_value=0.0,
            value=st.session_state.get("avg_price", 429.56),
            step=0.01,
            format="%.2f"
        )

        st.sidebar.header("🛡️ Hedge Setup")
        st.session_state.hedge_budget = st.sidebar.number_input(
            "Hedge Budget ($)",
            min_value=0.0,
            value=st.session_state.get("hedge_budget", 3000.0),
            step=50.0
        )
        st.session_state.budget_source = st.sidebar.radio(
            "Fund Hedge Using:",
            ("cash", "sell"),
            index=0 if st.session_state.get("budget_source", "cash") == "cash" else 1
        )

    st.sidebar.markdown("---")
    st.sidebar.info(f"Data fetched for: **{st.session_state.ticker}**")
