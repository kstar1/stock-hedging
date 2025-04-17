import numpy as np
import pandas as pd
from src.sim.put_breakeven_logic import calculate_now_capital, calculate_initial_capital

def simulate_put_net_pnl(selected_puts, price_range, current_price, shares, avg_price, hedge_budget, budget_source, use_market_price):
    """
    Simulates net P&L across a range of future prices based on selected PUTs.

    Args:
        selected_puts (pd.DataFrame): Must contain strike, mid_price, contracts
        price_range (np.array): Array of stock prices to simulate
        current_price (float): Current stock price
        shares (float): Number of shares held
        avg_price (float): Average purchase price
        hedge_budget (float): Max spend on PUTs
        budget_source (str): "cash" or "sell"
        use_market_price (bool): Use current price for initial cap baseline

    Returns:
        pd.DataFrame: Columns = ['price', 'net_pnl', 'initial_capital', 'now_capital']
    """
    premium_total = (selected_puts["mid_price"] * 100 * selected_puts["contracts"]).sum()
    contracts_total = (selected_puts["contracts"]).sum()

    initial_cap = calculate_initial_capital(
        current_price, shares, avg_price, hedge_budget,
        premium=0, contracts=contracts_total,  # total contracts used for hedge budget impact
        budget_source=budget_source,
        use_market_price=use_market_price
    )

    rows = []
    for future_price in price_range:
        total_now = 0
        for _, row in selected_puts.iterrows():
            total_now += calculate_now_capital(
                future_price,
                strike=row["strike"],
                premium=row["mid_price"],
                contracts=row["contracts"],
                shares=shares,
                budget_source=budget_source
            )

        net_pnl = total_now - initial_cap
        rows.append({
            "price": future_price,
            "initial_capital": initial_cap,
            "now_capital": total_now,
            "net_pnl": net_pnl
        })

    return pd.DataFrame(rows)
