# src/main.py

from data_fetcher import (
    get_stock_info,
    get_option_expirations,
    get_put_option_chain,
    get_historical_price
)
from option_analyzer import filter_puts, suggest_put
from hedge_simulator import simulate_hedge
from hedge_decision_simulator import simulate_decision
from visualizer import (
    plot_hedge_simulation,
    plot_decision_simulation,
    plot_breakeven_zone_map
)

from logger import log_simulation, log_decision
from utils import calculate_put_values, compute_breakeven_zones
from session_manager import clear_cache_files
from config.config_filters import FILTER_CONFIG

try:
    from config import NUM_SHARES
except ImportError:
    NUM_SHARES = float(input("Enter your number of TSLA shares: "))

selected_exp = None
current_puts = None
filtered_puts = None
selected_strike = None
selected_premium = None

def menu():
    print("\n=== TSLA Hedging Toolkit ===")
    print("1. View Stock Info")
    print("2. View Recent Price History")
    print("3. View Option Expiration Dates")
    print("4. View & Save Raw PUT Chain")
    print("5. View Filtered PUT Suggestions & Simulate")
    print("6. Simulate Capital-Preserving Hedge")
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
            selected_exp = input("\nEnter expiration date (YYYY-MM-DD): ")

        elif choice == "4":
            print("\n=== Available Expiration Dates ===")
            expirations = get_option_expirations()
            print(expirations)
            selected_exp = input("\nEnter expiration date (YYYY-MM-DD): ")
            current_puts = get_put_option_chain(expiration=selected_exp, save_to_file=True)
            print(f"\n✅ PUT chain saved to raw_put_chain_{selected_exp}.csv")

        elif choice == "5":
            print("\n=== Available Expiration Dates ===")
            expirations = get_option_expirations()
            print(expirations)
            selected_exp = input("\nEnter expiration date (YYYY-MM-DD): ")
            current_puts = get_put_option_chain(expiration=selected_exp)

            filtered_puts = filter_puts(current_puts, current_price=current_price, **FILTER_CONFIG)
            suggestions = suggest_put(filtered_puts)

            # Ensure 'premium' column exists
            filtered_puts["premium"] = filtered_puts["mid_price"]

            # Compute breakeven zones
            lower_breakevens = filtered_puts["strike"] - filtered_puts["premium"]
            upper_breakevens = current_price + (filtered_puts["premium"] * 100) / NUM_SHARES

            breakeven_df = filtered_puts.copy()
            breakeven_df["lower_breakeven"] = lower_breakevens
            breakeven_df["upper_breakeven"] = upper_breakevens

            plot_breakeven_zone_map(breakeven_df, selected_exp)

            # Save to log
            breakeven_df.to_csv(f"logs/breakeven_map_{selected_exp}.csv", index=False)
            print(f"\n📁 Breakeven zone data saved to logs/breakeven_map_{selected_exp}.csv")

            print("\n=== Filtered Suggestions ===")
            print(suggestions)

            try:
                # Compute and save breakeven map
                breakeven_df = compute_breakeven_zones(suggestions, current_price=current_price, num_shares=NUM_SHARES)
                breakeven_csv_path = f"logs/breakeven_map_{selected_exp}.csv"
                breakeven_df.to_csv(breakeven_csv_path, index=False)
                print(f"\n📁 Breakeven zone data saved to {breakeven_csv_path}")
                plot_breakeven_zone_map(breakeven_df, selected_exp)
                
                selected_idx = int(input("\nSelect index of suggested put to simulate (e.g., 0): "))
                selected_row = suggestions.iloc[selected_idx]
                selected_strike = selected_row["strike"]
                selected_premium = selected_row["mid_price"]
                contract_symbol = selected_row["contractSymbol"]

                print(f"\n🎯 Selected: {contract_symbol}")
                print(f"Strike: {selected_strike}, Premium: {selected_premium}")

                intrinsic, time = calculate_put_values(
                    strike=selected_strike,
                    market_price=current_price,
                    option_price=selected_premium
                )
                print(f"💡 Intrinsic Value: {intrinsic:.2f}")
                print(f"⏳ Time Value: {time:.2f}")

                df = simulate_hedge(
                    current_price=current_price,
                    num_shares=NUM_SHARES,
                    strike=selected_strike,
                    premium=selected_premium,
                    contracts=1
                )

                plot_hedge_simulation(
                    df,
                    strike=selected_strike,
                    premium=selected_premium,
                    expiration=selected_exp
                )

                # Explanation after graph
                print(f"\n📈 Green Zone 1 (Left): Profit when TSLA falls below {selected_strike - selected_premium:.2f}")
                print(f"You gain from exercising the PUT. Profit = ({selected_strike} - Market Price - {selected_premium}) * 100")

                print(f"\n📈 Green Zone 2 (Right): Profit when TSLA rises above breakeven on stock")
                print("Stock appreciation offsets cost of hedge.")

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
                print("✅ Simulation logged.")
            except Exception as e:
                print(f"❌ Invalid selection: {e}")

        elif choice == "6":
            try:
                avg_price = float(input("Your average TSLA purchase price: "))
                hedge_budget = float(input("Budget for buying PUTs (e.g., 1000): "))
                budget_source = input("Fund hedge using ('cash' or 'sell'): ").lower().strip()

                print("\n=== Available Expiration Dates ===")
                expirations = get_option_expirations()
                print(expirations)
                selected_exp = input("Enter expiration date (YYYY-MM-DD): ")

                current_puts = get_put_option_chain(expiration=selected_exp)
                filtered_puts = filter_puts(current_puts, current_price=current_price, **FILTER_CONFIG)
                suggestions = suggest_put(filtered_puts)

                print("\n=== Filtered Suggestions ===")
                print(suggestions)

                selected_idx = int(input("Select PUT to simulate with (index): "))
                selected_row = suggestions.iloc[selected_idx]

                strike = selected_row["strike"]
                premium = selected_row["mid_price"]

                df, meta = simulate_decision(
                    current_price=current_price,
                    avg_purchase_price=avg_price,
                    num_shares=NUM_SHARES,
                    strike=strike,
                    premium=premium,
                    hedge_budget=hedge_budget,
                    budget_source=budget_source
                )

                plot_decision_simulation(
                    df,
                    strike=strike,
                    premium=premium,
                    expiration=selected_exp,
                    roi=meta["roi_on_hedge"]
                )

                log_decision(
                    df=df,
                    strike=strike,
                    premium=premium,
                    expiration=selected_exp,
                    current_price=current_price,
                    avg_price=avg_price,
                    num_shares=NUM_SHARES,
                    hedge_budget=hedge_budget,
                    budget_source=budget_source,
                    meta=meta
                )

                print("✅ Decision simulation logged.")

            except Exception as e:
                print(f"❌ Error in simulation: {e}")

        elif choice == "0":
            print("Cleaning up temporary files...")
            clear_cache_files()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
