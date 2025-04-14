# src/hedge_simulator.py

import numpy as np
import pandas as pd

def simulate_hedge(current_price, num_shares, strike, premium, contracts=1):
    """
    Simulates P&L of portfolio with and without a PUT hedge.
    Returns a DataFrame with unhedged and hedged P&L across a range of future TSLA prices.
    """
    import numpy as np
    import pandas as pd

    price_range = np.linspace(current_price * 0.4, current_price * 1.6, 300)
    total_stock_cost = current_price * num_shares
    option_cost = contracts * 100 * premium

    unhedged_values = price_range * num_shares
    hedge_payouts = np.maximum(strike - price_range, 0) * contracts * 100
    hedged_values = unhedged_values + hedge_payouts - option_cost

    initial_value = total_stock_cost

    df = pd.DataFrame({
        "Future Price ($)": price_range,
        "Unhedged P&L ($)": unhedged_values - initial_value,
        "Hedged P&L ($)": hedged_values - initial_value,
    })

    return df
# src/visualizer.py (add or replace this function)

import matplotlib.pyplot as plt

def plot_hedge_simulation(df, strike, premium, expiration):
    """
    Plots unhedged and hedged P&L vs TSLA price.
    """
    # Smart detection of column names
    price_col = "TSLA_Price" if "TSLA_Price" in df.columns else "Future Price"
    hedged_col = "Hedged_PnL" if "Hedged_PnL" in df.columns else "Hedged P&L ($)"
    unhedged_col = "Unhedged_PnL" if "Unhedged_PnL" in df.columns else "Unhedged P&L ($)"

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df[price_col], df[unhedged_col], linestyle='--', color='blue', label='Unhedged P&L')
    ax.plot(df[price_col], df[hedged_col], color='orange', label='Hedged P&L')

    ax.axhline(0, color='gray', linestyle='--', linewidth=1)

    # Highlight profit/loss zones
    ax.fill_between(df[price_col], df[hedged_col], 0, where=(df[hedged_col] > 0), color='green', alpha=0.1)
    ax.fill_between(df[price_col], df[hedged_col], 0, where=(df[hedged_col] < 0), color='red', alpha=0.1)

    # Plot breakeven line
    breakeven = strike - premium
    ax.axvline(breakeven, linestyle=':', color='green', linewidth=1.5, label=f'Breakeven: ${breakeven:.2f}')

    ax.set_title(f"PUT Simulation | Strike: {strike} | Exp: {expiration} | Premium: ${premium:.2f}")
    ax.set_xlabel("Future TSLA Price ($)")
    ax.set_ylabel("Profit / Loss ($)")
    ax.legend()
    plt.tight_layout()
    plt.show()
