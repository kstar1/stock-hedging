import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_breakeven_zone_map(df, expiration_label):
    '''
    Plot breakeven zone map using lower and upper breakeven prices.
    Color bars by volume.
    '''
    import matplotlib.cm as cm
    import numpy as np

    df = df.copy()
    df = df[df["contracts"] > 0]  # Only plot options user can afford

    fig, ax = plt.subplots(figsize=(10, 6))

    x = df["strike"]
    y_low = df["lower_breakeven"]
    y_high = df["upper_breakeven"]
    volume = df["volume"]

    # Normalize volumes to color
    norm = plt.Normalize(volume.min(), volume.max())
    cmap = cm.get_cmap("viridis")  

    for xi, y1, y2, vol in zip(x, y_low, y_high, volume):
        ax.plot([xi, xi], [y1, y2], color=cmap(norm(vol)), linewidth=3)

    ax.set_title(f"Breakeven Zone Map - Exp: {expiration_label}")
    ax.set_xlabel("Strike Price ($)")
    ax.set_ylabel("Breakeven Prices ($)")
    ax.grid(True)

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Volume")

    return fig