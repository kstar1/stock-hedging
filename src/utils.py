import pandas as pd

def calculate_put_values(strike, market_price, option_price):
    intrinsic_value = max(strike - market_price, 0)
    time_value = option_price - intrinsic_value
    return intrinsic_value, time_value

def compute_breakeven_zones(df: pd.DataFrame, current_price: float, num_shares: float) -> pd.DataFrame:
    # Estimate breakeven zones
    shares_per_contract = 100
    total_shares = num_shares
    total_cost = df["mid_price"] * shares_per_contract

    df = df.copy()
    df["lower_breakeven"] = df["strike"] - df["mid_price"]
    df["upper_breakeven"] = ((df["mid_price"] * shares_per_contract) + (total_shares * current_price)) / total_shares
    return df
