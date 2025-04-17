import streamlit as st
import pandas as pd

from src.data.option_chain_provider import get_option_expirations, get_put_option_chain
from src.sim.option_filters import filter_puts
from src.sim.analytics import compute_breakeven_zones
from src.viz.put_breakeven_plot import plot_put_loss_zones

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
    '''
    st.markdown("🎯 **Filter PUTs by Moneyness and Volume**")
    # Moneyness Filter Slider
    strike_prices = raw_puts["strike"].dropna().astype(float)
    min_strike = strike_prices.min()
    max_strike = strike_prices.max()
    moneyness_min = int(min_strike - current_price)
    moneyness_max = int(max_strike - current_price)
    moneyness_range = st.slider(
        "Strike Price Range relative to Current Price ($)",
        min_value=moneyness_min,
        max_value=moneyness_max,
        value=(max(-20, moneyness_min), min(20, moneyness_max)),
        step=1
    )

    # Volume Filter Slider
    volume_threshold = st.slider(
        "📊 Minimum Volume Required",
        min_value=0,
        max_value=int(raw_puts["volume"].max()),
        value=100,
        step=10
    )
    #"""
    # Filter puts using sliders
    filtered_puts = filter_puts(
        raw_puts,
        current_price=current_price,
        min_volume=volume_threshold,
        moneyness_range=moneyness_range
    )
    #"""
    """
    st.subheader("🔎 Raw PUTs Debug Preview")
    st.write(raw_puts.shape)
    st.dataframe(raw_puts.head(100))

    # Optional: show distribution of strike prices vs current price
    st.write("Strike range:", raw_puts['strike'].min(), "to", raw_puts['strike'].max())
    st.write("Current price:", current_price)
    st.write("Volume stats — Min:", raw_puts['volume'].min(), "Max:", raw_puts['volume'].max())
    st.write("🔍 Filtered PUTs shape:", filtered_puts.shape)
    st.write("current_price:", current_price,"min_volume:", volume_threshold,"moneyness_range:", moneyness_range)
    """
    '''
    # === Intelligent Defaults from raw_puts ===
    strike_prices = raw_puts["strike"].dropna().astype(float)
    min_strike = strike_prices.min()
    max_strike = strike_prices.max()
    moneyness_range_full = (min_strike / current_price, max_strike / current_price)

    default_moneyness = (0.9, 1.1)
    default_volume = 500
    default_top_n = min(20, raw_puts.shape[0])  # cap default to 20
    max_possible_contracts = raw_puts.shape[0]

    # === Show Advanced Filter Toggle ===
    show_advanced = st.checkbox("🔧 Show Advanced Filtering", value=False)

    if show_advanced:
        with st.expander("🎛️ Advanced PUT Filtering"):
            moneyness_range = st.slider(
                "Moneyness Range (Strike ÷ Spot)",
                min_value=round(moneyness_range_full[0], 2),
                max_value=round(moneyness_range_full[1], 2),
                value=default_moneyness,
                step=0.01
            )
            volume_threshold = st.slider(
                "📊 Minimum Volume Required",
                min_value=0,
                max_value=int(raw_puts["volume"].max()),
                value=default_volume,
                step=10
            )
            max_contracts = st.slider(
                "📉 Max Contracts to Show",
                min_value=1,
                max_value=max_possible_contracts,
                value=default_top_n
            )
    else:
        moneyness_range = default_moneyness
        volume_threshold = default_volume
        max_contracts = default_top_n

    # === Apply Filters ===
    filtered_puts = filter_puts(
        raw_puts,
        current_price=current_price,
        min_volume=volume_threshold,
        moneyness_range=moneyness_range
    )

    filtered_puts = filtered_puts.head(max_contracts)

    if filtered_puts.empty:
        st.warning("No PUT contracts matched the filter criteria.")
        return

    #strike_min = current_price + moneyness_range[0]
    #strike_max = current_price + moneyness_range[1]

    # Decision regarding the use of market price for initial capital
    use_market_price = st.sidebar.toggle(
        "📈 Use Market Price to Calculate Initial Capital?",
        value=True,
        help="If disabled, initial capital is based on average purchase price instead."
    )

    # Compute breakeven zones
    breakeven_df = compute_breakeven_zones(
        filtered_puts,
        current_price=current_price,
        num_shares=num_shares,
        avg_price=avg_price,
        hedge_budget=hedge_budget,
        budget_source=budget_source,
        use_market_price=use_market_price
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

