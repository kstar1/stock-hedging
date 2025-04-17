
import streamlit as st
import pandas as pd
import numpy as np

from src.data.option_chain_provider import get_option_expirations, get_put_option_chain
from src.sim.option_filters import filter_puts
from src.sim.analytics import compute_breakeven_zones
from src.sim.put_simulation_logic import simulate_put_net_pnl
from src.viz.put_breakeven_plot import plot_put_loss_zones
from src.viz.put_simulation_plot import plot_net_pnl_zone

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

    # === Intelligent Defaults from raw_puts ===
    strike_prices = raw_puts["strike"].dropna().astype(float)
    min_strike = strike_prices.min()
    max_strike = strike_prices.max()
    moneyness_range_full = (min_strike / current_price, max_strike / current_price)

    default_moneyness = (0.9, 1.1)
    default_volume = 500
    default_top_n = min(20, raw_puts.shape[0])  # cap default to 20
    max_possible_contracts = raw_puts.shape[0]

    show_advanced = st.checkbox("🔧 Show Advanced Filtering", value=False)
    if show_advanced:
        with st.expander("🎛️ Advanced PUT Filtering"):
            moneyness_range = st.slider("Moneyness Range (Strike ÷ Spot)", min_value=round(moneyness_range_full[0], 2),
                                        max_value=round(moneyness_range_full[1], 2), value=default_moneyness, step=0.01)
            volume_threshold = st.slider("📊 Minimum Volume Required", min_value=0,
                                         max_value=int(raw_puts["volume"].max()), value=default_volume, step=10)
            max_contracts = st.slider("📉 Max Contracts to Show", min_value=1,
                                      max_value=max_possible_contracts, value=default_top_n)
    else:
        moneyness_range = default_moneyness
        volume_threshold = default_volume
        max_contracts = default_top_n

    filtered_puts = filter_puts(raw_puts, current_price, min_volume=volume_threshold, moneyness_range=moneyness_range)
    filtered_puts = filtered_puts.head(max_contracts)

    if filtered_puts.empty:
        st.warning("No PUT contracts matched the filter criteria.")
        return

    use_market_price = st.sidebar.toggle("📈 Use Market Price to Calculate Initial Capital?",
                                         value=True,
                                         help="If disabled, initial capital is based on average purchase price instead.")

    breakeven_df = compute_breakeven_zones(filtered_puts, current_price, num_shares, avg_price, hedge_budget,
                                           budget_source, use_market_price)

    if breakeven_df.empty:
        st.warning("No PUT contracts have valid breakeven zones.")
        return

    with st.expander("📘 What does this chart show?", expanded=True):
        st.markdown("""
        The breakeven zone chart shows for each PUT option the **range of market prices** where your **capital would be below the initial capital**.

        - Each **vertical line** is a PUT contract's breakeven zone.
        - The **upper breakeven** is when remaining stocks alone recover initial investment.
        - The **lower breakeven** is when the PUT option protects enough to cover the losses.
        - **Color gradient** reflects trade volume—helps identify liquidity.

        ⚠️ *Only contracts within your hedge budget are included.*
        """)

    st.markdown("📌 Select Contracts to Show in Chart (tick to display):")
    contract_labels = breakeven_df["contractSymbol"]
    selected_labels = []
    cols = st.columns(4)
    for idx, label in enumerate(contract_labels):
        with cols[idx % 4]:
            if st.checkbox(f"{label}", key=f"chk_{label}", value=True):
                selected_labels.append(label)

    chart_df = breakeven_df.loc[breakeven_df["contractSymbol"].isin(selected_labels)].copy()
    st.pyplot(plot_put_loss_zones(chart_df, current_price))

    # === Net P&L Simulation ===
    st.markdown("## 📊 Simulate Net P&L")
    st.markdown("Select how many contracts you'd like to simulate for each PUT:")

    selected_contracts = []
    for i, row in chart_df.iterrows():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{row['contractSymbol']}** @ Strike: ${row['strike']}")
        with col2:
            num = st.number_input(f"Contracts", min_value=0, max_value=10, value=0, key=f"num_{i}")
            if num > 0:
                selected_contracts.append({
                    "contractSymbol": row['contractSymbol'],
                    "strike": row['strike'],
                    "mid_price": row['mid_price'],
                    "contracts": num
                })

    if selected_contracts:
        selected_df = pd.DataFrame(selected_contracts)
        price_range = np.linspace(current_price * 0.5, current_price * 1.5, 100)
        sim_df = simulate_put_net_pnl(selected_df, price_range, current_price, num_shares, avg_price, hedge_budget,
                                      budget_source, use_market_price)
        st.pyplot(plot_net_pnl_zone(sim_df))