import matplotlib.pyplot as plt
import numpy as np

def plot_hedge_simulation(df, strike, premium, expiration):
    future_prices = df["Future Price ($)"]
    hedged_pnl = df["Hedged P&L ($)"]
    unhedged_pnl = df["Unhedged P&L ($)"]

    fig = plt.figure(figsize=(12, 6))
    plt.plot(future_prices, unhedged_pnl, linestyle='--', color='blue', label="Unhedged P&L")
    plt.plot(future_prices, hedged_pnl, color='orange', label="Hedged P&L")

    # Fill profit and loss regions
    plt.fill_between(future_prices, hedged_pnl, where=(hedged_pnl >= 0), color='green', alpha=0.1)
    plt.fill_between(future_prices, hedged_pnl, where=(hedged_pnl < 0), color='red', alpha=0.1)

    # Breakeven
    breakeven = strike - premium
    plt.axvline(breakeven, linestyle=':', color='green', label=f"Breakeven: ${breakeven:.2f}")

    plt.axhline(0, color='gray', linewidth=1)
    plt.xlabel("Future TSLA Price ($)")
    plt.ylabel("Profit / Loss ($)")
    plt.title(f"PUT Simulation | Strike: {strike} | Exp: {expiration} | Premium: ${premium:.2f}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    return fig

def plot_decision_simulation(df, strike, premium, expiration, roi=None):
    price_col = "Future Price ($)" if "Future Price ($)" in df.columns else "Future Price"
    net_col = "Net P&L ($)" if "Net P&L ($)" in df.columns else "Net PnL"

    fig = plt.figure(figsize=(12, 7))
    plt.plot(df[price_col], df[net_col], label="Total Portfolio P&L", color="blue")

    plt.axhline(0, linestyle="--", color="gray")
    plt.fill_between(df[price_col], df[net_col], 0, where=(df[net_col] >= 0), interpolate=True, color='green', alpha=0.1)
    plt.fill_between(df[price_col], df[net_col], 0, where=(df[net_col] < 0), interpolate=True, color='red', alpha=0.1)

    plt.title(f"Hedge Decision | Strike {strike}, Premium {premium}, Exp {expiration}")
    plt.xlabel("Future TSLA Price ($)")
    plt.ylabel("Net P&L ($)")

    if roi is not None:
        plt.text(
            df[price_col].iloc[-1] * 0.6,
            max(df[net_col]) * 0.95,
            f"ROI on hedge: {roi:.2f}%",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="lightyellow", edgecolor="gray")
        )

    plt.legend()
    plt.tight_layout()

    return fig