# test_imports.py
print("Attempting imports...")
try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import yfinance as yf # Ensure it's installed

    from config.settings import DEFAULT_TICKER, FILTER_CONFIG

    from src.data.stock_data_provider import get_stock_info, get_historical_price
    from src.data.option_chain_provider import get_option_expirations, get_put_option_chain
    # from src.data.data_models import ... # If you created models

    from src.sim.option_filters import filter_puts, suggest_put
    from src.sim.analytics import calculate_put_values, compute_breakeven_zones
    from src.sim.hedge_simulator import simulate_hedge, simulate_decision

    # Only import plotting functions, don't need matplotlib if just testing imports
    from src.viz.price_charts import plot_hedge_simulation # Assuming you might move it here later
    from src.viz.option_charts import plot_breakeven_zone_map
    from src.viz.simulation_plots import plot_decision_simulation, plot_hedge_simulation # Or keep hedge plot here

    # Import UI placeholders if you created them
    # from src.ui.sidebar import build_sidebar
    # from src.ui.tabs.stock_info_tab import render_stock_info_tab
    # ... etc ...

    print("✅ All basic imports successful!")

    # Optional: Try calling a simple cached function (requires internet)
    print("\nAttempting simple data fetch (requires internet)...")
    info = get_stock_info(DEFAULT_TICKER)
    if info and info.get("current_price"):
        print(f"✅ Fetched stock info for {DEFAULT_TICKER}. Current Price: {info['current_price']}")
    else:
        print(f"⚠️ Could not fetch valid stock info for {DEFAULT_TICKER}.")

    expirations = get_option_expirations(DEFAULT_TICKER)
    if expirations:
         print(f"✅ Fetched {len(expirations)} option expirations for {DEFAULT_TICKER}.")
    else:
        print(f"⚠️ Could not fetch option expirations for {DEFAULT_TICKER}.")


except ImportError as e:
    print(f"\n❌ ImportError: {e}")
    print("👉 Check file paths, function names, and __init__.py files.")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")