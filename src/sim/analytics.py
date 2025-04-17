import pandas as pd
import numpy as np
from src.sim.put_breakeven_logic import solve_breakeven

def compute_breakeven_zones(df, current_price, num_shares, avg_price, hedge_budget, budget_source):
    df = df.copy()
    shares_per_contract = 100
    initial_capital = num_shares * avg_price

    df["hedge_cost"] = df["mid_price"] * shares_per_contract
    df["contracts"] = (hedge_budget // df["hedge_cost"]).astype(int)
    df["total_hedge_cost"] = df["contracts"] * df["hedge_cost"]

    df["lower_breakeven"] = np.nan
    df["upper_breakeven"] = np.nan

    for index, row in df.iterrows():
        contracts = row["contracts"]
        strike_price = row["strike"]
        premium_per_share = row["mid_price"]

        if contracts > 0:
            # Use new solve_breakeven function from logic module
            df["breakeven_note"] = ""
            lb, ub, reason = solve_breakeven(
                current_price, strike_price, premium_per_share, contracts,
                num_shares, avg_price, hedge_budget, budget_source, mode="both"
            )
            df.loc[index, "lower_breakeven"] = lb
            df.loc[index, "upper_breakeven"] = ub
            df.loc[index, "breakeven_note"] = reason

    return df