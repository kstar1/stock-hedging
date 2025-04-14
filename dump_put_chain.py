# dump_put_chain.py

import pandas as pd
from data_fetcher import get_put_option_chain
from data_fetcher import get_stock_info

expiration = "2025-04-17"
puts_df = get_put_option_chain(expiration=expiration)
stock_info = get_stock_info()
current_price = stock_info["current_price"]

puts_df["mid_price"] = (puts_df["bid"] + puts_df["ask"]) / 2
puts_df["current_price"] = current_price
puts_df["intrinsic_value"] = puts_df["strike"] - current_price
puts_df["time_value"] = puts_df["mid_price"] - puts_df["intrinsic_value"]
puts_df = puts_df[[
    "contractSymbol", "strike", "lastPrice", "bid", "ask", "mid_price",
    "volume", "openInterest", "impliedVolatility", "intrinsic_value", "time_value"
]]

# Save to file
puts_df.to_csv("full_put_chain_2025-04-17.txt", index=False)
print("✅ Full put option chain saved to 'full_put_chain_2025-04-17.txt'")
