# src/visualizer.py

import matplotlib.pyplot as plt
import pandas as pd

def plot_hedge_simulation(df: pd.DataFrame, title: str = "Portfolio P&L with Put Hedge"):
    """
    Plots profit/loss for unhedged and hedged portfolio across future TSLA prices.
    """
    plt.figure(figsize=(10, 6))

    plt.plot(df["TSLA_Price"], df["Unhedged_PnL"], label="Unhedged P&L", linestyle="--")
    plt.plot(df["TSLA_Price"], df["Hedged_PnL"], label="Hedged P&L", linewidth=2)

    plt.axhline(0, color="gray", linestyle=":")
    plt.xlabel("Future TSLA Price ($)")
    plt.ylabel("Profit / Loss ($)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
