import streamlit as st
import pandas as pd

from config.settings import FILTER_CONFIG
from src.data.option_chain_provider import get_put_option_chain, get_option_expirations
from src.sim.option_filters import filter_puts, suggest_put
from src.sim.analytics import compute_breakeven_zones, calculate_put_values
from src.viz.option_charts import plot_breakeven_zone_map

def render_put_chain_tab():
    import math
    import streamlit as st
    import pandas as pd

    from config.settings import FILTER_CONFIG
    from src.data.option_chain_provider import get_put_option_chain, get_option_expirations
    from src.sim.option_filters import filter_puts
    from src.sim.analytics import compute_breakeven_zones, calculate_put_values
    from src.viz.option_charts import plot_breakeven_zone_map

    st.header("PUT Option Chain Explorer")

    ticker = st.session_state.ticker
    current_price = st.session_state.stock_info.get("current_price", 0)
    expirations = get_option_expirations(ticker)

    if not expirations:
        st.warning(f"No option expiration dates found for {ticker}.")
        return

    if st.session_state.selected_expiration in expirations:
        selected_exp_index = expirations.index(st.session_state.selected_expiration)
    else:
        selected_exp_index = 0

    st.session_state.selected_expiration = st.selectbox(
        "Select Expiration Date", expirations, index=selected_exp_index
    )

    if not st.session_state.selected_expiration:
        st.warning("No expiration date selected.")
        return

    try:
        puts_df = get_put_option_chain(ticker, st.session_state.selected_expiration)
        st.session_state.option_chain = puts_df

        if puts_df.empty:
            st.warning(f"No PUT options data found for {st.session_state.selected_expiration}.")
            return

        filtered_puts = filter_puts(
            puts_df,
            current_price=current_price,
            min_volume=FILTER_CONFIG.get("min_volume", 50),
            moneyness_range=tuple(FILTER_CONFIG.get("moneyness_range", [0.90, 1.10]))
        )

        if "mid_price" not in filtered_puts.columns and \
           "bid" in filtered_puts.columns and \
           "ask" in filtered_puts.columns:
            filtered_puts["mid_price"] = (filtered_puts["bid"] + filtered_puts["ask"]) / 2

        if filtered_puts.empty:
            st.warning("No PUT contracts matched the filter criteria.")
            return

        st.session_state.filtered_options = filtered_puts

        breakeven_df = compute_breakeven_zones(
            filtered_puts.copy(),
            current_price=current_price,
            num_shares=st.session_state.shares,
            avg_price=st.session_state.avg_price,
            hedge_budget=st.session_state.hedge_budget,
            budget_source=st.session_state.budget_source,
        )

        st.subheader("Breakeven Zone Map")
        st.info("Vertical lines show price zones where you'd break even with PUT + stock. Color = volume.")
        try:
            fig = plot_breakeven_zone_map(breakeven_df, st.session_state.selected_expiration)
            st.pyplot(fig)
        except Exception as plot_e:
            st.error(f"Failed to generate plot: {plot_e}")

        st.subheader("Filtered PUT Options")
        display_cols = ['contractSymbol', 'strike', 'mid_price', 'volume', 'impliedVolatility', 'lastPrice', 'bid', 'ask']
        display_df = filtered_puts[[col for col in display_cols if col in filtered_puts.columns]].copy()
        display_df.sort_values(by="strike", inplace=True)

        # Prompt + better radio labels
        st.markdown("👀 **Click one of the contracts below to see when you'll recover your original capital (😢 if never):**")

        display_df["label"] = display_df["strike"].apply(lambda x: f"Strike ${x:.2f}")
        contract_labels = display_df["label"].tolist()
        label_to_symbol = dict(zip(contract_labels, display_df["contractSymbol"].tolist()))

        selected_label = st.radio(
            "Available Contracts",
            contract_labels,
            index=None,
            key="put_selector"
        )

        selected_symbol = label_to_symbol.get(selected_label)

        if selected_symbol:
            selected_row = display_df[display_df['contractSymbol'] == selected_symbol].iloc[0]
            st.session_state.selected_put_contract = selected_row.to_dict()
            st.session_state.run_simulation = True

            try:
                intrinsic, time = calculate_put_values(
                    strike=selected_row["strike"],
                    market_price=current_price,  # ✅ Fixed argument
                    option_price=selected_row["mid_price"]
                )
                st.success(
                    f"Selected: **{selected_symbol}** | "
                    f"Strike: ${selected_row['strike']:.2f}, "
                    f"Premium: ${selected_row['mid_price']:.2f} | "
                    f"Intrinsic: ${intrinsic:.2f}, Time Value: ${time:.2f}"
                )

                # === Breakeven Explanation ===
                shares = st.session_state.shares
                avg_price = st.session_state.avg_price
                initial_capital = shares * avg_price
                hedge_budget = st.session_state.hedge_budget
                budget_source=st.session_state.budget_source
                current_price = st.session_state.stock_info.get("current_price", 0)

                strike = selected_row['strike']
                premium = selected_row['mid_price']
                shares_per_contract = 100

                hedge_cost_per_contract = premium * shares_per_contract
                contracts = math.floor(hedge_budget / hedge_cost_per_contract)
                protected_shares = contracts * shares_per_contract
                #unprotected_shares = max(0, shares - protected_shares)

                # Copied from src/sim/analytics.py
                num_shares=st.session_state.shares
                num_protected_shares = contracts * shares_per_contract

                if budget_source == "sell":
                    shares_sold = (hedge_cost_per_contract * contracts) / current_price if current_price > 0 else 0
                    remaining_shares = shares - shares_sold
                    unprotected_shares = max(0, num_shares - shares_sold)
                else:  # budget_source == "cash"
                    shares_sold = 0.0  # Explicitly set shares_sold to 0 for cash
                    remaining_shares = shares  # remaining_shares is initial shares for cash
                    unprotected_shares = max(0, num_shares - num_protected_shares)

                if protected_shares > 0:
                    if unprotected_shares - protected_shares != 0:
                        lower_breakeven = (initial_capital + protected_shares * (premium - strike)) / (unprotected_shares - protected_shares)
                    else:
                        lower_breakeven = strike - premium - (initial_capital / protected_shares)
                else:
                    lower_breakeven = None

                #shares_sold = hedge_budget / current_price if current_price > 0 else 0
                #remaining_shares = shares - shares_sold
                upper_breakeven = initial_capital / remaining_shares if remaining_shares > 0 else None

                """
                st.write(f"DEBUG: budget_source: {budget_source}")
                st.write(f"DEBUG: shares: {shares}")
                st.write(f"DEBUG: avg_price: {avg_price}")
                st.write(f"DEBUG: initial_capital: {initial_capital}")
                st.write(f"DEBUG: hedge_budget: {hedge_budget}")
                st.write(f"DEBUG: contracts: {contracts}")
                st.write(f"DEBUG: strike: {strike}")
                st.write(f"DEBUG: premium: {premium}")
                st.write(f"DEBUG: protected_shares: {protected_shares}")
                st.write(f"DEBUG: unprotected_shares: {unprotected_shares}")
                st.write(f"DEBUG: lower_breakeven: {lower_breakeven}")
                st.write(f"DEBUG: current_price: {current_price}")
                st.write(f"DEBUG: shares_sold: {shares_sold}")
                st.write(f"DEBUG: remaining_shares: {remaining_shares}")
                st.write(f"DEBUG: upper_breakeven: {upper_breakeven}")
                """
                st.markdown("### 📘 Breakeven Explanation")
                st.markdown(f'''
#### 💰 Your Starting Position

You hold **{shares:.2f} shares** of TSLA, purchased at an average of **${avg_price:.2f}**.  
This gives you an initial capital base of:

```
Initial Capital = {shares:.2f} × ${avg_price:.2f} = ${initial_capital:,.2f}
```

---

#### 🛡️ Your Hedge Setup

You allocated **${hedge_budget:,.2f}** to hedge your portfolio by purchasing **{contracts} PUT contracts** at:
- Strike Price = **${strike:.2f}**
- Premium = **${premium:.2f}**
- Protected Shares = **{protected_shares}**
- Unprotected Shares = **{unprotected_shares:.2f}**

---

#### 🔻 Lower Breakeven (if stock falls)

PUTs protect you when TSLA drops. Here's how we compute the price where your PUTs and unprotected shares exactly recover your original capital:

```
Lower Breakeven = {strike:.2f} - {premium:.2f} - (Initial Capital / Protected Shares)  
                = {strike:.2f} - {premium:.2f} - ({initial_capital:.2f} / {protected_shares})  
                = **${lower_breakeven:.2f}**
```

---

#### 🔺 Upper Breakeven (if stock rises)

You chose to fund the hedge using **{budget_source.upper()}**.
''')

                if budget_source == "sell":
                    st.markdown(f'''
In this case, you sold shares to raise your hedge budget:

```
Shares Sold = Hedge Budget / Market Price = ${hedge_budget:,.2f} / ${current_price:.2f} = {shares_sold:.2f}
Remaining Shares = {shares:.2f} - {shares_sold:.2f} = {remaining_shares:.2f}
Upper Breakeven = Initial Capital / Remaining Shares = ${initial_capital:,.2f} / {remaining_shares:.2f} = **${upper_breakeven:.2f}**
```
''')
                else:
                    st.markdown(f'''
Since you're funding the hedge with external cash, you keep all **{shares:.2f} shares**.

```
Upper Breakeven = Initial Capital / Shares = ${initial_capital:,.2f} / {shares:.2f} = **${upper_breakeven:.2f}**
```
''')
                st.markdown(f"""
#### 💰 Initial Capital

- You bought **{shares:.2f} shares** at an average price of **${avg_price:.2f}**  
- Your total starting capital is **${initial_capital:,.2f}**

---

#### 🛡️ Hedge Setup

- Hedge Budget: **${hedge_budget:,.2f}**
- PUTs Bought: **{contracts} contract(s)** at:
  - Strike Price = **${strike:.2f}**
  - Premium = **${premium:.2f}**
- Protected Shares = **{protected_shares}**
- Unprotected Shares = **{unprotected_shares:.2f}**

---

#### 📉 Lower Breakeven (if stock falls)

PUTs are exercised to offset your capital loss.  
We solve this:

```
Lower Breakeven = K - P - (Initial Capital / Protected Shares)
                = {strike:.2f} - {premium:.2f} - ({initial_capital:,.2f} / {protected_shares})
                = ${lower_breakeven:.2f}
```

If TSLA falls **below ${lower_breakeven:.2f}**, your losses are offset by PUT gains.

---

#### 📈 Upper Breakeven (if stock rises)

Your PUTs expire worthless, but your remaining shares gain in value.  
We solve:

```
Shares Sold for Hedge = H / P_mkt = {hedge_budget:,.2f} / {current_price:.2f} = {shares_sold:.2f}
Remaining Shares = {shares:.2f} - {shares_sold:.2f} = {remaining_shares:.2f}
Upper Breakeven = Initial Capital / Remaining Shares
                = {initial_capital:,.2f} / {remaining_shares:.2f}
                = ${upper_breakeven:.2f}
```

If TSLA rises **above ${upper_breakeven:.2f}**, your remaining shares recover your capital.
""")

            except Exception as e:
                st.warning(f"Could not calculate intrinsic/time value: {e}")
        else:
            st.session_state.selected_put_contract = None
            st.session_state.run_simulation = False

    except Exception as e:
        st.error(f"Error processing option chain: {e}")
        st.session_state.option_chain = pd.DataFrame()
        st.session_state.filtered_options = pd.DataFrame()
        st.session_state.selected_put_contract = None
        st.session_state.run_simulation = False