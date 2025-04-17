import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

def plot_put_loss_zones(df, current_price):
    '''
    Visualizes loss-making breakeven zones for each PUT strike.
    df is expected to come from analytics.compute_breakeven_zones()
    and must include:
        ['strike', 'lower_breakeven', 'upper_breakeven', 'volume']
    '''

    df = df.copy()
    df = df[df['contracts'] > 0]  # Only plot contracts user can afford
    df.dropna(subset=['strike'], inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    strikes = df['strike'].astype(float)
    vol = df['volume'].fillna(0).astype(float)
    norm = plt.Normalize(vol.min(), vol.max())
    cmap = cm.get_cmap("viridis")

    for _, row in df.iterrows():
        strike = row["strike"]
        vol = row["volume"]
        ub = row["upper_breakeven"]
        lb = row["lower_breakeven"]

        # Normalize volume for colormap
        vol_norm = (vol - df['volume'].min()) / (df['volume'].max() - df['volume'].min() + 1e-5)
        color = cmap(norm(vol)) if not np.isnan(vol) else 'gray'

        if pd.notna(lb) and pd.notna(ub):
            ax.vlines(x=strike, ymin=lb, ymax=ub, color=color, linewidth=6)
        elif pd.notna(lb):
            ax.plot(strike, lb, 'o', color=color, markersize=12)
        elif pd.notna(ub):
            ax.plot(strike, ub, 'o', color=color, markersize=12)
        else:
            # Optional: annotate contract with no breakeven zone
            note = row.get("breakeven_note", "")
            ax.annotate("⚠", (strike, 5), rotation=90, fontsize=10, ha="center")

    ax.axhline(current_price, color='black', linestyle='--', label='Current TSLA Price')
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("TSLA Market Price")
    ax.set_title("Loss Zones by PUT Strike Price")
    ax.grid(True)

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Volume (Shading)")

    return fig