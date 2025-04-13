# src/logger.py

import pandas as pd
from datetime import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/hedge_logs.csv')

def log_simulation(df: pd.DataFrame, strike, premium, expiration, current_price, num_shares):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hedged_min = df["Hedged_PnL"].min()
    hedged_max = df["Hedged_PnL"].max()
    unhedged_min = df["Unhedged_PnL"].min()
    unhedged_max = df["Unhedged_PnL"].max()

    log_entry = pd.DataFrame([{
        "timestamp": timestamp,
        "expiration": expiration,
        "strike": strike,
        "premium": premium,
        "num_shares": num_shares,
        "current_price": current_price,
        "hedged_min_pnl": hedged_min,
        "hedged_max_pnl": hedged_max,
        "unhedged_min_pnl": unhedged_min,
        "unhedged_max_pnl": unhedged_max
    }])

    if os.path.exists(LOG_FILE):
        log_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(LOG_FILE, index=False)
