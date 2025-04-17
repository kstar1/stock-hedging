import plotly.graph_objects as go
import pandas as pd

def plot_net_pnl_zone(df: pd.DataFrame):
    """
    Interactive Net P&L chart using Plotly.

    Args:
        df: DataFrame with columns [price, net_pnl]
    Returns:
        Plotly Figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["price"],
        y=df["net_pnl"],
        mode="lines",
        name="Net P&L",
        line=dict(color="blue"),
        hovertemplate="Price: $%{x:.2f}<br>P&L: $%{y:.2f}"
    ))

    fig.add_trace(go.Scatter(
        x=df["price"],
        y=[0] * len(df),
        mode="lines",
        line=dict(color="gray", dash="dot"),
        name="Break-even"
    ))

    fig.update_layout(
        title="Simulated Net P&L from Selected PUTs",
        xaxis_title="Stock Price ($)",
        yaxis_title="Net P&L ($)",
        height=600
    )

    return fig
