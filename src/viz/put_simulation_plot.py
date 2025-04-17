import matplotlib.pyplot as plt
import numpy as np

def plot_net_pnl_zone(df):
    """
    Plots net P&L across stock prices with green/red shading.

    Args:
        df (pd.DataFrame): Must contain ['price', 'net_pnl']
    Returns:
        fig: Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot net P&L line
    ax.plot(df["price"], df["net_pnl"], label="Net P&L", color="blue", linewidth=2)

    # Zero line
    ax.axhline(0, color="black", linestyle="--", linewidth=1, label="Break-even")

    # Fill profit/loss zones
    ax.fill_between(df["price"], df["net_pnl"], where=df["net_pnl"] >= 0, interpolate=True, color="green", alpha=0.3, label="Profit")
    ax.fill_between(df["price"], df["net_pnl"], where=df["net_pnl"] < 0, interpolate=True, color="red", alpha=0.3, label="Loss")

    # Axes and grid
    ax.set_xlabel("Stock Price ($)")
    ax.set_ylabel("Net P&L ($)")
    ax.set_title("📈 Simulated Net P&L from Selected PUTs")
    ax.grid(True)
    ax.legend()

    return fig
