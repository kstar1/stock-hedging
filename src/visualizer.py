import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Option 5 hedge simulation plot ---
def plot_hedge_simulation(df, strike, premium, expiration):
    future_prices = df["Future Price ($)"]
    hedged_pnl = df["Hedged P&L ($)"]
    unhedged_pnl = df["Unhedged P&L ($)"]

    plt.figure(figsize=(12, 6))
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
    plt.show()

# --- Option 6 capital-preserving hedge plot ---
def plot_decision_simulation(df, strike, premium, expiration, roi=None):
    price_col = "Future Price ($)" if "Future Price ($)" in df.columns else "Future Price"
    net_col = "Net P&L ($)" if "Net P&L ($)" in df.columns else "Net PnL"

    plt.figure(figsize=(12, 7))
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
    plt.show()

# --- Option 5: Breakeven zone map with volume-based vertical lines ---
def plot_breakeven_zone_map(df: pd.DataFrame, expiration: str):
    strikes = df["strike"]
    premiums = df["mid_price"]
    volumes = df["volume"]
    lower = df["lower_breakeven"]
    upper = df["upper_breakeven"]

    # Percentile thresholds
    v80 = np.percentile(volumes, 80)
    v20 = np.percentile(volumes, 20)

    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Plot breakeven ranges per strike
    for i in range(len(df)):
        vol = volumes.iloc[i]
        color = "green" if vol >= v80 else "orange" if vol > v20 else "red"
        ax1.plot([strikes.iloc[i], strikes.iloc[i]], [lower.iloc[i], upper.iloc[i]], color=color, linewidth=3)

    ax1.set_xlabel("Strike Price ($)")
    ax1.set_ylabel("Breakeven Prices ($)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Premium (no line joining)
    ax2 = ax1.twinx()
    ax2.scatter(strikes, premiums, color='gray', label="Premium", marker='x')
    ax2.set_ylabel("Premium ($)", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')

    # Build and show custom legend
    lines = [
        plt.Line2D([0], [0], color="green", linewidth=3, label=f"High Volume (≥ {v80:.0f})"),
        plt.Line2D([0], [0], color="orange", linewidth=3, label=f"Medium Volume ({v20:.0f}–{v80:.0f})"),
        plt.Line2D([0], [0], color="red", linewidth=3, label=f"Low Volume (≤ {v20:.0f})"),
        plt.Line2D([0], [0], linestyle='None', marker='x', color='gray', label="Premium")
    ]
    ax1.legend(handles=lines, loc="upper left")

    plt.title(f"Breakeven Zones vs Strike Prices | Exp: {expiration}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
