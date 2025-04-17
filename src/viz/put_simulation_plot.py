import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_net_pnl_zone(df: pd.DataFrame):
    """
    Interactive Net P&L chart using Plotly.

    Args:
        df: DataFrame with columns [price, net_pnl]
    Returns:
        Plotly Figure
    """
    fig = go.Figure()

    colors = np.where(df["net_pnl"] >= 0, "rgba(0,200,0,0.2)", "rgba(200,0,0,0.2)")

    for i in range(len(df) - 1):
        fig.add_trace(go.Scatter(
            x=[df["price"].iloc[i], df["price"].iloc[i+1]],
            y=[df["net_pnl"].iloc[i], df["net_pnl"].iloc[i+1]],
            fill='tozeroy',
            fillcolor=colors[i],
            line=dict(width=0),
            hoverinfo='skip',
            showlegend=False
        ))

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
