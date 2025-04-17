import pandas as pd
from src.sim.put_breakeven_logic import solve_breakeven
from src.viz.put_breakeven_plot import plot_put_loss_zones

# Base data (applies to both tests)
df = pd.DataFrame({
    "strike": [200, 220, 240],
    "mid_price": [5.0, 7.5, 10.0],
    "volume": [100, 300, 150]
})

# Common input values
price = 260  # current TSLA price
hedge_budget = 3000
budget_source = "cash"
contracts = 1

# --- TEST 1: Zero shares, non-zero avg price ---
shares = 0
avg_price = 429.56

lb_ub_results = [solve_breakeven(price, row["strike"], row["mid_price"], contracts, shares, avg_price, hedge_budget, budget_source, mode="both") for _, row in df.iterrows()]
df["lower_breakeven"] = [res[0] if res else None for res in lb_ub_results]
df["upper_breakeven"] = [res[1] if res else None for res in lb_ub_results]
df["contracts"] = contracts

fig1 = plot_put_loss_zones(df, current_price=price)
fig1.savefig("test_zero_shares_nonzero_avg_price.png")

# --- TEST 2: Non-zero shares, zero avg price ---
shares = 34.65
avg_price = 0

lb_ub_results = [solve_breakeven(price, row["strike"], row["mid_price"], contracts, shares, avg_price, hedge_budget, budget_source, mode="both") for _, row in df.iterrows()]
df["lower_breakeven"] = [res[0] if res else None for res in lb_ub_results]
df["upper_breakeven"] = [res[1] if res else None for res in lb_ub_results]
df["contracts"] = contracts

fig2 = plot_put_loss_zones(df, current_price=price)
fig2.savefig("test_nonzero_shares_zero_avg_price.png")

print("✅ Saved: test_zero_shares_nonzero_avg_price.png and test_nonzero_shares_zero_avg_price.png")
