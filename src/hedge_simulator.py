# src/hedge_simulator.py

import numpy as np
import pandas as pd

def simulate_hedge(
    current_price: float,
    num_shares: float,
    strike: float,
    premium: float,
    contracts: int = 1,
    contract_size: int = 100,
    price_range: tuple = (100, 400),
    num_points: int = 100
) -> pd.DataFrame:
    """
    Simulates portfolio performance with and without a put hedge.
    """
    future_prices = np.linspace(price_range[0], price_range[1], num_points)
    
    # Unhedged value = number of shares * future price
    unhedged_values = future_prices * num_shares

    # Hedged value = unhedged + (put payoff - premium)
    put_payoffs = np.maximum(strike - future_prices, 0) * contracts * contract_size
    total_premium = premium * contracts * contract_size
    hedged_values = unhedged_values + (put_payoffs - total_premium)

    # Starting value of your position today
    initial_value = current_price * num_shares

    # Profit/loss calculation
    df = pd.DataFrame({
        "TSLA_Price": future_prices,
        "Unhedged_Value": unhedged_values,
        "Hedged_Value": hedged_values,
        "Unhedged_PnL": unhedged_values - initial_value,
        "Hedged_PnL": hedged_values - initial_value
    })

    return df
