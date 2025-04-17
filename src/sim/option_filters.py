import pandas as pd

def filter_puts(
    puts_df: pd.DataFrame,
    current_price: float,
    min_volume: int = 100,
    moneyness_range: tuple = (0.8, 1.3)
) -> pd.DataFrame:
    """
    Filter PUT options for hedging based on:
    - Sufficient volume
    - Strike close to or above current price
    - Reasonable moneyness
    """
    puts_df = puts_df.copy()

    # Calculate mid price if not already present
    if "mid_price" not in puts_df.columns:
        puts_df["mid_price"] = (puts_df["bid"] + puts_df["ask"]) / 2
        puts_df["mid_price"] = puts_df["mid_price"].fillna(puts_df["lastPrice"])
        puts_df.loc[puts_df["mid_price"] == 0, "mid_price"] = puts_df["lastPrice"]

    puts_df["intrinsic_value"] = puts_df["strike"] - current_price
    puts_df["time_value"] = puts_df["mid_price"] - puts_df["intrinsic_value"]

    # Filter 1: strike within 95% to 105% of current price
    min_strike = current_price * moneyness_range[0]
    max_strike = current_price * moneyness_range[1]
    puts_df = puts_df[puts_df["strike"].between(min_strike, max_strike)]

    # Filter 2: must have sufficient volume
    puts_df = puts_df[puts_df["volume"] >= min_volume]

    # Filter 3: must have non-negative mid_price
    puts_df = puts_df[puts_df["mid_price"] > 0]

    # Sort by moneyness (closest to ATM)
    puts_df["abs_diff"] = abs(puts_df["strike"] - current_price)
    puts_df = puts_df.sort_values("abs_diff")

    return puts_df.reset_index(drop=True)

def suggest_put(filtered_df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Return top N PUTs with reasonable hedging potential
    """
    columns = [
        "contractSymbol", "strike", "lastPrice", "bid", "ask",
        "mid_price", "volume", "impliedVolatility"
    ]
    return filtered_df[columns].head(top_n)