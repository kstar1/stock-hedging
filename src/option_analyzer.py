# src/option_analyzer.py
import pandas as pd

def filter_puts(
    puts_df: pd.DataFrame,
    current_price: float,
    max_days_to_expiry: int = 60,
    min_volume: int = 10,
    max_bid_ask_spread: float = 10.0,
    moneyness_range: tuple = (0.8, 1.0)
):
    """
    Filters put options based on:
    - Expiry within `max_days_to_expiry` (handled in caller via expiration selection)
    - Strike between 80% and 100% of current price (default moneyness)
    - Minimum trading volume
    - Reasonable bid-ask spread
    """
    # Calculate additional metrics
    puts_df["mid_price"] = (puts_df["bid"] + puts_df["ask"]) / 2
    puts_df["spread"] = puts_df["ask"] - puts_df["bid"]
    puts_df["moneyness"] = puts_df["strike"] / current_price

    # Apply filters
    filtered = puts_df[
        (puts_df["volume"] >= min_volume) &
        (puts_df["spread"] <= max_bid_ask_spread) &
        (puts_df["moneyness"] >= moneyness_range[0]) &
        (puts_df["moneyness"] <= moneyness_range[1])
    ].copy()

    # Sort by best mid price (lowest premium for highest protection)
    filtered.sort_values(by=["mid_price", "strike"], ascending=[True, False], inplace=True)

    return filtered.reset_index(drop=True)


def suggest_put(filtered_puts: pd.DataFrame, top_n: int = 3):
    """
    Suggest top N put options based on filtered results
    """
    return filtered_puts.head(top_n)[[
        "contractSymbol", "strike", "lastPrice", "bid", "ask", "mid_price", "volume", "impliedVolatility"
    ]]
