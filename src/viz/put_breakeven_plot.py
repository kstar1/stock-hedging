import plotly.graph_objects as go
import pandas as pd

def plot_put_loss_zones(df: pd.DataFrame, current_price: float):
    """
    Interactive breakeven zone visualization using Plotly.

    Args:
        df: DataFrame with strike, volume, lower_breakeven, upper_breakeven
        current_price: float

    Returns:
        Plotly Figure
    """
    df = df.copy()
    df = df[df['contracts'] > 0].dropna(subset=["strike"])
    
    fig = go.Figure()

    # Add each breakeven as a line or point
    for _, row in df.iterrows():
        strike = row["strike"]
        lb = row["lower_breakeven"]
        ub = row["upper_breakeven"]
        vol = row["volume"]
        color = "rgba(0, 150, 255, 0.6)"  # color uniform for now

        if pd.notna(lb) and pd.notna(ub):
            fig.add_trace(go.Scatter(
                x=[strike, strike], y=[lb, ub],
                mode='lines',
                line=dict(width=6, color=color),
                name=f"{strike} | Vol: {vol}",
                hovertemplate=f"<b>Strike: ${strike}</b><br>Volume: {vol}<br>Lower: {lb:.2f}<br>Upper: {ub:.2f}"
            ))
        elif pd.notna(lb):
            fig.add_trace(go.Scatter(
                x=[strike], y=[lb],
                mode="markers",
                marker=dict(size=12, color="orange", symbol="triangle-down"),
                name=f"{strike} | Vol: {vol}",
                hovertemplate=f"<b>Strike: ${strike}</b><br>Only Lower Breakeven: {lb:.2f}<br>Volume: {vol}"
            ))
        elif pd.notna(ub):
            fig.add_trace(go.Scatter(
                x=[strike], y=[ub],
                mode="markers",
                marker=dict(size=12, color="purple", symbol="triangle-up"),
                name=f"{strike} | Vol: {vol}",
                hovertemplate=f"<b>Strike: ${strike}</b><br>Only Upper Breakeven: {ub:.2f}<br>Volume: {vol}"
            ))

    # Horizontal line = current price
    fig.add_hline(y=current_price, line_dash="dot", line_color="black", annotation_text="Current Price")

    fig.update_layout(
        title="Loss Zones by PUT Strike Price",
        xaxis_title="Strike Price ($)",
        yaxis_title="Market Price ($)",
        height=600
    )

    return fig
