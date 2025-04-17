from put_breakeven_logic import solve_breakeven

# Example contract data
test_cases = [
    {
        "label": "Normal - SELL",
        "price": 250,
        "strike": 250,
        "premium": 10,
        "contracts": 2,
        "shares": 34.65,
        "avg_price": 429.56,
        "hedge_budget": 3000,
        "budget_source": "sell"
    },
    {
        "label": "Normal - CASH",
        "price": 250,
        "strike": 250,
        "premium": 10,
        "contracts": 2,
        "shares": 34.65,
        "avg_price": 429.56,
        "hedge_budget": 3000,
        "budget_source": "cash"
    },
    {
        "label": "No Shares - CASH",
        "price": 250,
        "strike": 250,
        "premium": 10,
        "contracts": 2,
        "shares": 0.0,
        "avg_price": 0.0,
        "hedge_budget": 3000,
        "budget_source": "cash"
    },
    {
        "label": "No Shares - SELL",
        "price": 250,
        "strike": 250,
        "premium": 10,
        "contracts": 2,
        "shares": 0.0,
        "avg_price": 0.0,
        "hedge_budget": 3000,
        "budget_source": "sell"
    },
    {
        "label": "Insufficient Budget - SELL",
        "price": 250,
        "strike": 250,
        "premium": 50,
        "contracts": 3,
        "shares": 50,
        "avg_price": 200,
        "hedge_budget": 500,
        "budget_source": "sell"
    },
    {
        "label": "Deep OTM PUTs",
        "price": 250,
        "strike": 100,
        "premium": 1,
        "contracts": 5,
        "shares": 34.65,
        "avg_price": 429.56,
        "hedge_budget": 1000,
        "budget_source": "cash"
    },
]

for case in test_cases:
    print(f"--- {case['label'].upper()} ---")
    params = {k: v for k, v in case.items() if k != "label"}
    ub = solve_breakeven(**params, mode="upper")
    lb = solve_breakeven(**params, mode="lower")
    print(f"Upper Breakeven: {ub}")
    print(f"Lower Breakeven: {lb}\n")