import numpy as np
from scipy.optimize import fsolve

def calculate_initial_capital(price, shares, avg_price, hedge_budget, premium, contracts, budget_source, use_market_price=True):
    share_value = shares * price if use_market_price else shares * avg_price
    initial_cap = share_value + hedge_budget if budget_source == "cash" else share_value
    return initial_cap

def calculate_now_capital(price, strike, premium, contracts, shares, budget_source):
    hedge_cost = premium * contracts * 100
    put_payoff = max(0, (strike - premium - price)) * contracts * 100

    if budget_source == "sell":
        shares_sold = hedge_cost / price
        remaining_shares = shares - shares_sold
    else:
        remaining_shares = shares

    stock_value = remaining_shares * price
    return put_payoff + stock_value

def solve_breakeven(price, strike, premium, contracts, shares, avg_price, hedge_budget, budget_source, mode="both", use_market_price=True):
    try:
        if contracts <= 0 or premium <= 0:
            return (np.nan, np.nan, "no contracts (contracts <= 0 or premium <= 0)")

        hedge_cost = premium * contracts * 100
        if budget_source == "sell" and shares * price < hedge_cost:
            return (np.nan, np.nan, "Can't buy the contracts from selling your shares")

        if budget_source == "cash" and hedge_budget < hedge_cost:
            return (np.nan, np.nan, "Can't buy contracts from the cash (not enough)")

        initial_cap = calculate_initial_capital(
            price, shares, avg_price, hedge_budget, premium, contracts, budget_source, use_market_price
        )

        def difference(p):
            if p <= 0:
                return 1e6
            capital_now = calculate_now_capital(p, strike, premium, contracts, shares, budget_source)
            return capital_now - initial_cap

        lower_breakeven = None
        upper_breakeven = None

        if shares == 0 or avg_price == 0:
            # Only lower breakeven is possible (PUT-only hedge)
            guess = strike - 50
            lower_result = fsolve(difference, guess)[0]
            if 0 < lower_result < 10000:
                return (lower_result, np.nan, "Only lower breakeven exists (PUT-only hedge)")
            else:
                return (np.nan, np.nan, "Breakeven could not be solved (PUT-only hedge)")
        else:
            if mode in ("both", "lower"):
                guess = strike - 50
                lower_result = fsolve(difference, guess)[0]
                if 0 < lower_result < 10000:
                    lower_breakeven = lower_result

            if mode in ("both", "upper"):
                guess = strike + 50
                upper_result = fsolve(difference, guess)[0]
                if 0 < upper_result < 10000:
                    upper_breakeven = upper_result

            explanation = "Standard hedge (stock + PUT)"
            if lower_breakeven is None and upper_breakeven is None:
                explanation = "Could not solve either breakeven"
            elif lower_breakeven is None:
                explanation = "Only upper breakeven exists"
            elif upper_breakeven is None:
                explanation = "Only lower breakeven exists"

            return (lower_breakeven, upper_breakeven, explanation)

    except Exception as e:
        return (np.nan, np.nan, f"Exception occurred: {str(e)}")
