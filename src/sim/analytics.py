import pandas as pd
import numpy as np

def calculate_put_values(strike, market_price, option_price):
    intrinsic_value = max(strike - market_price, 0)
    time_value = option_price - intrinsic_value
    return intrinsic_value, time_value


def compute_breakeven_zones(
    df: pd.DataFrame,
    current_price: float,
    num_shares: float,
    avg_price: float,
    hedge_budget: float,
    budget_source: str,
) -> pd.DataFrame:
    """
    Calculates breakeven zones based on user's holdings and hedge budget,
    considering the logic of selling shares to buy protective put options.

    Assumptions:
    - The user utilizes the 'hedge_budget' to purchase PUT options.
    - Standard put option contracts cover 100 shares.
    - The lower breakeven point is calculated based on the scenario where the put options are exercised,
      offsetting losses on the *initially held* shares. It considers the net profit from the puts
      (strike - market price - premium) on the protected portion.
    - The upper breakeven point assumes the put options expire worthless. The remaining shares
      (after hypothetically selling some to fund the puts) need to cover the initial capital.
    - The number of contracts bought is the maximum integer number affordable within the hedge budget
      for each put option listed.
    - Transaction costs are not considered.

    Symbols:
    - df: DataFrame of PUT options with 'strike' and 'mid_price' columns.
    - current_price (P_mkt_sell): Current market price of the stock (used as the selling price for hypothetical hedge funding).
    - num_shares (S_initial): Initial number of shares owned by the user.
    - avg_price (A): Average purchase price of user's shares.
    - hedge_budget (H): Amount allocated to buy PUT contracts.
    - strike (K): Strike price of the PUT option.
    - mid_price (P): Mid-price (premium) of the PUT option per share.
    - shares_per_contract: Number of shares covered by one contract (100).
    - contracts: Number of PUT option contracts purchased.
    - lower_breakeven: The market price at which the user's net position (remaining shares + put option payoff) equals the initial capital.
    - upper_breakeven: The market price at which the value of the remaining shares (after hypothetically selling some) equals the initial capital (assuming puts expire worthless).

    Returns:
        df : DataFrame with 'contracts', 'lower_breakeven', and 'upper_breakeven' columns added.
    """
    df = df.copy()
    shares_per_contract = 100
    initial_capital = num_shares * avg_price

    df["hedge_cost"] = df["mid_price"] * shares_per_contract
    df["contracts"] = (hedge_budget // df["hedge_cost"]).astype(int)
    df["total_hedge_cost"] = df["contracts"] * df["hedge_cost"]

    df["lower_breakeven"] = np.nan
    df["upper_breakeven"] = np.nan

    for index, row in df.iterrows():
        contracts = int(row["contracts"])
        strike_price = row["strike"]
        premium_per_share = row["mid_price"]

        num_protected_shares = contracts * shares_per_contract

        if budget_source == "sell":
            shares_sold = row["total_hedge_cost"] / current_price if current_price > 0 else 0
            num_unprotected_shares = max(0, num_shares - shares_sold)
        else:  # budget_source == "cash"
            num_unprotected_shares = max(0, num_shares - num_protected_shares)

        # Lower Breakeven Calculation
        if num_protected_shares > 0:
            if num_unprotected_shares - num_protected_shares != 0:
                df.loc[index, "lower_breakeven"] = (initial_capital + num_protected_shares * (premium_per_share - strike_price)) / (num_unprotected_shares - num_protected_shares)
            else:
                df.loc[index, "lower_breakeven"] = strike_price - premium_per_share - (initial_capital / num_protected_shares)
        else:
            df.loc[index, "lower_breakeven"] = None

        # Upper Breakeven Calculation
        if budget_source == "sell":
            shares_sold = row["total_hedge_cost"] / current_price if current_price > 0 else 0
            remaining_shares_upper = num_shares - shares_sold
        else:  # budget_source == "cash"
            remaining_shares_upper = num_shares
        df.loc[index, "upper_breakeven"] = initial_capital / remaining_shares_upper if remaining_shares_upper > 0 else None

    return df