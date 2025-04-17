import streamlit as st
import pandas as pd

from src.data.option_chain_provider import get_option_expirations, get_put_option_chain
from src.sim.option_filters import filter_puts
from src.sim.analytics import compute_breakeven_zones
from src.viz.put_breakeven_plot import plot_put_loss_zones
#from src.sim.put_breakeven_logic import calculate_put_values

def render_put_chain_tab():
    st.header("📉 PUT Option Chain Explorer")

    ticker = st.session_state.ticker
    current_price = st.session_state.stock_info.get("current_price", 0)
    num_shares = st.session_state.get("shares", 0)
    avg_price = st.session_state.get("avg_price", 0)
    hedge_budget = st.session_state.get("hedge_budget", 0)
    budget_source = st.session_state.get("budget_source", "cash")

    expirations = get_option_expirations(ticker)
    if not expirations:
        st.warning(f"No option expiration dates found for {ticker}.")
        return

    selected_exp = st.selectbox("Select Expiration Date", expirations)
    raw_puts = get_put_option_chain(ticker, selected_exp)
    if raw_puts is None or raw_puts.empty:
        st.warning("No PUT option data found.")
        return

    filtered_puts = filter_puts(raw_puts, current_price)
    if filtered_puts.empty:
        st.warning("No PUT contracts matched the filter criteria.")
        return

    # Filter PUTs by volume and moneyness
    # Automatically determine moneyness range from available strike prices
    strike_prices = filtered_puts["strike"].dropna().astype(float)
    min_strike = strike_prices.min()
    max_strike = strike_prices.max()
    moneyness_min = int(min_strike - current_price)
    moneyness_max = int(max_strike - current_price)

    st.markdown("🎯 **Filter PUTs by Moneyness and Volume**")

    # Moneyness Filter Slider
    moneyness_range = st.slider(
        "Strike Price Range relative to Current Price ($)",
        min_value=moneyness_min,
        max_value=moneyness_max,
        value=(max(-20, moneyness_min), min(20, moneyness_max)),
        step=1
    )
    strike_min = current_price + moneyness_range[0]
    strike_max = current_price + moneyness_range[1]

    # Volume Filter Slider
    volume_threshold = st.slider(
        "📊 Minimum Volume Required",
        min_value=int(filtered_puts["volume"].min()),
        max_value=int(filtered_puts["volume"].max()),
        value=100,
        step=10
    )

    # Apply both filters to puts
    filtered_puts = filtered_puts[
        (filtered_puts["strike"].between(strike_min, strike_max)) &
        (filtered_puts["volume"] >= volume_threshold)
    ]

    # Compute breakeven zones
    breakeven_df = compute_breakeven_zones(
        filtered_puts,
        current_price=current_price,
        num_shares=num_shares,
        avg_price=avg_price,
        hedge_budget=hedge_budget,
        budget_source=budget_source
    )

    if breakeven_df.empty:
        st.warning("No PUT contracts have valid breakeven zones.")
        return

    # Display Explanation Panel
    with st.expander("📘 What does this chart show?", expanded=True):
        st.markdown("""
        The breakeven zone chart shows for each PUT option the **range of market prices** where your **capital would be below the initial capital**.

        - Each **vertical line** is a PUT contract's breakeven zone.
        - The **upper breakeven** is when remaining stocks alone recover initial investment.
        - The **lower breakeven** is when the PUT option protects enough to cover the losses.
        - **Color gradient** reflects trade volume—helps identify liquidity.

        ⚠️ *Only contracts within your hedge budget are included.*
        """)

    # Show multiselect for contract filtering
    contract_labels = breakeven_df["contractSymbol"]

    st.markdown("📌 Select Contracts to Show in Chart (tick to display):")

    selected_labels = []
    cols = st.columns(4)
    for idx, label in enumerate(contract_labels):
        with cols[idx % 4]:
            if st.checkbox(f"{label}", key=f"chk_{label}", value=True):
                selected_labels.append(label)

    chart_df = breakeven_df.loc[breakeven_df["contractSymbol"].isin(selected_labels)].copy()
    st.pyplot(plot_put_loss_zones(chart_df, current_price))

