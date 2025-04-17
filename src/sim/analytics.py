
import pandas as pd
from src.sim.put_breakeven_logic import solve_breakeven

def compute_breakeven_zones(df: pd.DataFrame, current_price: float, num_shares: float,
                             avg_price: float, hedge_budget: float, budget_source: str,
                             use_market_price: bool = True) -> pd.DataFrame:
    df = df.copy()
    df["contracts"] = (hedge_budget // (df["mid_price"] * 100)).astype(int)
    df["total_cost"] = df["contracts"] * df["mid_price"] * 100

    breakevens = df.apply(
        lambda row: solve_breakeven(
            price=current_price,
            strike=row["strike"],
            premium=row["mid_price"],
            contracts=row["contracts"],
            shares=num_shares,
            avg_price=avg_price,
            hedge_budget=hedge_budget,
            budget_source=budget_source,
            use_market_price=use_market_price
        ),
        axis=1
    )

    df["lower_breakeven"] = [b[0] for b in breakevens]
    df["upper_breakeven"] = [b[1] for b in breakevens]
    df["explanation"] = [b[2] for b in breakevens]

    return df
