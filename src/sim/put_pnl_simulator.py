
import pandas as pd
import numpy as np

def simulate_put_pnl_strict(selected_puts, price_range, current_price, shares, avg_price,
                             hedge_budget, budget_source, use_market_price):
    '''
    Simulates net P&L based on selected PUTs.
    This version uses explicit cost-based logic (user PDF logic).

    Returns:
        df with columns: price, initial_capital, now_capital, net_pnl
    '''

    # Step 1: Compute hedge cost
    hedge_cost = (selected_puts["mid_price"] * 100 * selected_puts["contracts"]).sum()
    contracts_total = selected_puts["contracts"].sum()

    if hedge_cost > hedge_budget:
        raise ValueError("Hedge cost exceeds hedge budget")

    # Step 2: Initial capital
    if use_market_price:
        stock_value_initial = shares * current_price
    else:
        stock_value_initial = shares * avg_price

    if budget_source == "cash":
        initial_capital = stock_value_initial + hedge_budget
    else:
        initial_capital = stock_value_initial

    rows = []

    for future_price in price_range:
        total_put_payoff = 0

        for _, row in selected_puts.iterrows():
            strike = row["strike"]
            premium = row["mid_price"]
            contracts = row["contracts"]
            payoff = max(0, strike - future_price - premium) * contracts * 100
            total_put_payoff += payoff

        if budget_source == "sell":
            #shares_sold = hedge_cost / future_price
            shares_sold = hedge_cost / current_price
            shares_remaining = shares - shares_sold # Shares are always sold at current price
            stock_value = shares_remaining * future_price
            now_capital = total_put_payoff + stock_value
        else:  # cash
            stock_value = shares * future_price
            leftover_cash = hedge_budget - hedge_cost
            now_capital = total_put_payoff + stock_value + leftover_cash

        net_pnl = now_capital - initial_capital

        rows.append({
            "price": future_price,
            "initial_capital": initial_capital,
            "now_capital": now_capital,
            "net_pnl": net_pnl
        })

    return pd.DataFrame(rows), hedge_cost
