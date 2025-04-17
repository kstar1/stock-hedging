import streamlit as st
import pandas as pd
import numpy as np

from src.data.option_chain_provider import get_option_expirations, get_put_option_chain
from src.sim.option_filters import filter_puts
from src.sim.analytics import compute_breakeven_zones
from src.viz.put_breakeven_plot import plot_put_loss_zones
from src.viz.put_simulation_plot import plot_net_pnl_zone
from src.sim.put_pnl_simulator import simulate_put_pnl_strict

def render_put_chain_tab():
    st.header("📉 PUT Option Chain Explorer")
    st.markdown("This tool helps you evaluate the **impact of PUT options on your portfolio's performance** across future stock prices.")

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

    # === Filtering Defaults and Controls ===
    strike_prices = raw_puts["strike"].dropna().astype(float)
    min_strike = strike_prices.min()
    max_strike = strike_prices.max()
    left = current_price - min_strike
    right = max_strike - current_price

    default_moneyness = (current_price - 0.2 * left, current_price + 0.2 * right)
    moneyness_range_full = (min_strike, max_strike)
    default_volume = 500
    default_top_n = min(20, raw_puts.shape[0])
    max_possible_contracts = raw_puts.shape[0]

    show_advanced = st.checkbox("🔧 Show Advanced Filtering", value=False)
    if show_advanced:
        with st.expander("🎛️ Advanced PUT Filtering"):
            moneyness_range = st.slider("Moneyness Range", min_value=round(moneyness_range_full[0], 2),
                                        max_value=round(moneyness_range_full[1], 2),
                                        value=default_moneyness, step=0.01)
            volume_threshold = st.slider("📊 Minimum Volume Required", min_value=0,
                                         max_value=int(raw_puts["volume"].max()), value=default_volume, step=10)
            max_contracts = st.slider("📉 Max Contracts to Show", min_value=1,
                                      max_value=max_possible_contracts, value=default_top_n)
    else:
        moneyness_range = default_moneyness
        volume_threshold = default_volume
        max_contracts = default_top_n

    moneyness_ratio_range = (moneyness_range[0] / current_price, moneyness_range[1] / current_price)
    filtered_puts = filter_puts(raw_puts, current_price, min_volume=volume_threshold, moneyness_range=moneyness_ratio_range)
    filtered_puts = filtered_puts.head(max_contracts)

    if filtered_puts.empty:
        st.warning("No PUT contracts matched the filter criteria.")
        return

    use_market_price = st.sidebar.toggle("📈 Use Market Price to Calculate Initial Capital?", value=True,
                                         help="If disabled, initial capital is based on average purchase price instead.")

    breakeven_df = compute_breakeven_zones(
        filtered_puts, current_price, num_shares, avg_price, hedge_budget,
        budget_source, use_market_price
    )

    if breakeven_df.empty:
        st.warning("No PUT contracts have valid breakeven zones.")
        return

    # === Breakeven Zone Chart ===
    with st.expander("📘 What does this chart show?", expanded=True):
        st.markdown("""
        The breakeven zone chart shows for each PUT option the **range of market prices** where your **capital would be below the initial capital**.

        - Each **vertical line** is a PUT contract's breakeven zone.
        - Each lower triangle represents the minimum value of stock price where the PUT option is profitable.
        - The **upper breakeven** is when remaining stocks alone recover initial investment.
        - The **lower breakeven** is when the PUT option protects enough to cover the losses.
        ⚠️ *Only contracts within your hedge budget are included.*
        """)

    st.markdown("### 📌 Select Contracts to Show in Chart (`{Strike | Premium}`)")

    selected_labels = []
    cols = st.columns(4)
    for idx, row in breakeven_df.iterrows():
        strike = row["strike"]
        premium = row["mid_price"]
        label = row["contractSymbol"]
        display = f"${strike} | {premium}"
        with cols[idx % 4]:
            if st.checkbox(display, value=True, key=f"show_{label}"):
                selected_labels.append(label)

    chart_df = breakeven_df[breakeven_df["contractSymbol"].isin(selected_labels)].copy()
    st.plotly_chart(plot_put_loss_zones(chart_df, current_price), use_container_width=True)

    # === P&L Simulation UI ===
    st.markdown("## 📊 Simulate Net P&L")

    with st.expander("💡 What does Net P&L mean?", expanded=False):
        st.markdown("""
        This chart simulates how your portfolio value changes as the stock price moves. It accounts for:

        - Your existing TSLA shares
        - The PUT options you've selected
        - Whether you used **cash or stock sales** to fund them

        Green = Profit. Red = Loss. Use this to fine-tune your hedge strategy.
        """)

    selected_contracts = []
    col_group = st.columns([4, 1, 1])

    with col_group[0]:
        st.markdown("### Select Contracts to Simulate (P&L)")

    with col_group[1]:
        st.markdown("### Qty")

    hedge_cost = 0
    for i, row in chart_df.iterrows():
        symbol = row['contractSymbol']
        strike = row['strike']
        price = row['mid_price']

        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"{strike} | {price:.2f}")
        with col2:
            count = st.number_input(" ", min_value=0, max_value=10, value=0, key=f"sim_{i}")
        with col3:
            st.text("")

        if count > 0:
            selected_contracts.append({
                "contractSymbol": symbol,
                "strike": strike,
                "mid_price": price,
                "contracts": count
            })
            hedge_cost += count * price * 100

    col_space, col_cost = st.columns([6, 1])
    with col_cost:
        st.markdown(f"💰 **Hedge Cost**: `${hedge_cost:,.2f}`")

    if selected_contracts:
        simulate = st.button("📊 Simulate Net P&L", key="simulate_net_final")

        if simulate:
            if hedge_cost > hedge_budget:
                st.error("🚫 Hedge cost exceeds your hedge budget.")
            else:
                selected_df = pd.DataFrame(selected_contracts)
                price_range = np.linspace(current_price * 0.5, current_price * 1.5, 100)
                sim_df, _ = simulate_put_pnl_strict(
                    selected_df,
                    price_range,
                    current_price,
                    num_shares,
                    avg_price,
                    hedge_budget,
                    budget_source,
                    use_market_price
                )
                st.plotly_chart(plot_net_pnl_zone(sim_df), use_container_width=True)
