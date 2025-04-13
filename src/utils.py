def calculate_put_values(strike, market_price, option_price):
    """
    Calculate intrinsic and time value for a put option.

    Parameters:
        strike (float): The strike price of the option
        market_price (float): The current market price of the stock
        option_price (float): The price (premium) paid for the option

    Returns:
        (tuple): intrinsic_value, time_value
    """
    intrinsic_value = max(strike - market_price, 0)
    time_value = option_price - intrinsic_value
    return intrinsic_value, time_value
