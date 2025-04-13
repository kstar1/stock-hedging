# src/test_run.py (Optional)
from hedge_simulator import simulate_hedge
from visualizer import plot_hedge_simulation

df = simulate_hedge(
    current_price=252.93,
    num_shares=34.65,
    strike=240,
    premium=5.0,
    contracts=1
)

plot_hedge_simulation(df)
