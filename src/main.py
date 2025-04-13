# src/main.py

import json
import os

from data_fetcher import (
    get_stock_info,
    get_option_expirations,
    get_put_option_chain,
    get_historical_price
)
from option_analyzer import filter_puts, suggest_put
from hedge_simulator import simulate_hedge
from visualizer import plot_hedge_simulation
from logger import log_simulation
from utils import calculate_put_values
from session_manager import save_selected_expiration, get_selected_expiration, clear_session
from cleanup import clean_up_logs_and_cache

try:
    from config import NUM_SHARES
except ImportError:
    NUM_SHARES = float(input("Enter your number of TSLA shares: "))

# Load filter config
with open("config_filters.json", "r") as f:
    FILTER_CONFIG = json.load(f)

selected_exp = get_selected_expiration()
current_puts = None
filtered_puts = None
selected_strike = None
selected_premium = None

def menu():
    print("\n=== TSLA Hedging Toolkit ===")
    print("1. View Stock Info")
    print("2. View Recent Price History")
    print("3. View Option Expiration Dates")
    print("4. View Raw PUT Chain")
    print("5. View Filtered PUT Suggestions")
    print("6. Simulate & Plot Hedge")
    print("0. Exit")

def main():
    global selected_exp, current_puts, filtered_puts, selected_strike, selected_premium

    info = get_stock_info()
    current_price = info["current_price"]

    while True:
        menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print("\n=== TSLA Stock Info ===")
            for k, v in info.items():
                print(f"{k}: {v}")

        elif choice == "2":
            print("\n=== TSLA Recent Price History ===")
            hist = get_historical_price()
            print(hist.tail())

        elif choice == "3":
            print("\n=== Available Expiration Dates ===")
            expirations = get_option_expirations()
            print(expirations)
            selected_exp = input("\nSelect expiration (YYYY-MM-DD): ")
            save_selected_expiration(selected_exp)

        elif choice == "4":
            if not selected_exp:
                print("Please select expiration first (option 3).")
                continue
            current_puts = get_put_option_chain(expiration=selected_exp)
            print(f"\n=== Raw PUT Chain for {selected_exp} ===")
            print(current_puts[["contractSymbol", "strike", "lastPrice", "bid", "ask", "volume", "impliedVolatility"]].head(10))

        elif choice == "5":
            if current_puts is None:
                print("Please fetch raw puts first (option 4).")
                continue

            filtered_puts = filter_puts(
                puts_df=current_puts,
                current_price=current_price,
                moneyness_range=FILTER_CONFIG["moneyness_range"],
                max_bid_ask_spread=FILTER_CONFIG["max_bid_ask_spread"],
                min_volume=FILTER_CONFIG["min_volume"]
            )
            suggestions = suggest_put(filtered_puts)
            print("\n=== Filtered Suggestions ===")
            print(suggestions)

            try:
                selected_idx = int(input("\nSelect index of suggested put to simulate (e.g., 0): "))
                selected_row = suggestions.iloc[selected_idx]
                selected_strike = selected_row["strike"]
                selected_premium = selected_row["mid_price"]
                print(f"\n🎯 Selected Strike: {selected_strike}, Premium: {selected_premium}")

                intrinsic, time = calculate_put_values(
                    strike=selected_strike,
                    market_price=current_price,
                    option_price=selected_premium
                )
                print(f"💡 Intrinsic Value: {intrinsic:.2f}")
                print(f"⏳ Time Value: {time:.2f}")
                if time > intrinsic:
                    print("🧠 Most of this option’s value is time-based — you're paying for protection against big moves before expiration.")
                else:
                    print("🛡️ This option is mostly intrinsic — meaning it would be profitable if exercised today.")
            except Exception as e:
                print(f"❌ Invalid selection: {e}")
                selected_strike = None

        elif choice == "6":
            if selected_strike is None or selected_premium is None:
                print("Please select a put option first (option 5).")
                continue

            df = simulate_hedge(
                current_price=current_price,
                num_shares=NUM_SHARES,
                strike=selected_strike,
                premium=selected_premium,
                contracts=1
            )
            plot_hedge_simulation(df)

            intrinsic, time = calculate_put_values(
                strike=selected_strike,
                market_price=current_price,
                option_price=selected_premium
            )

            log_simulation(
                df=df,
                strike=selected_strike,
                premium=selected_premium,
                expiration=selected_exp,
                current_price=current_price,
                num_shares=NUM_SHARES,
                intrinsic_value=intrinsic,
                time_value=time
            )
            print("✅ Hedge simulation logged successfully.")

        elif choice == "0":
            print("Cleaning up session...")
            clear_session()
            clean_up_logs_and_cache()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
