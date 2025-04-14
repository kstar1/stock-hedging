import numpy as np
import pandas as pd

def simulate_decision(
    current_price: float,
    avg_purchase_price: float,
    num_shares: float,
    strike: float,
    premium: float,
    hedge_budget: float,
    budget_source: str = "cash"  # "cash" or "sell"
) -> tuple[pd.DataFrame, dict]:
    shares_per_contract = 100
    option_cost = premium * shares_per_contract
    max_contracts = int(hedge_budget // option_cost)

    if max_contracts == 0:
        raise ValueError("Hedge budget too small to buy even one contract.")

    total_put_cost = max_contracts * option_cost

    if budget_source.lower() == "sell":
        shares_sold = hedge_budget / current_price
        remaining_shares = num_shares - shares_sold
        if remaining_shares <= 0:
            raise ValueError("Not enough shares remaining after funding hedge from sales.")
    else:
        shares_sold = 0
        remaining_shares = num_shares

    price_range = np.linspace(current_price * 0.8, current_price * 1.2, 100)
    hedge_payout = np.maximum(strike - price_range, 0) * shares_per_contract * max_contracts
    stock_pnl = (price_range - avg_purchase_price) * remaining_shares
    net_pnl = stock_pnl + hedge_payout - total_put_cost

    df = pd.DataFrame({
        "Future Price ($)": price_range,
        "Net P&L ($)": net_pnl
    })

    # ROI on hedge
    worst_price = price_range[0]
    hedge_profit = hedge_payout[0] - total_put_cost
    roi_on_hedge = (hedge_profit / total_put_cost) * 100

    # Breakeven points (approx)
    breakeven_low = strike - premium
    breakeven_high = avg_purchase_price + (total_put_cost / remaining_shares)

    metadata = {
        "contracts_purchased": max_contracts,
        "total_put_cost": total_put_cost,
        "roi_on_hedge": roi_on_hedge,
        "shares_sold": shares_sold,
        "remaining_shares": remaining_shares,
        "breakeven_low": breakeven_low,
        "breakeven_high": breakeven_high,
        "hedge_profit": hedge_profit
    }

    return df, metadata
