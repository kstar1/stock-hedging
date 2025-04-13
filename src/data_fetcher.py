# src/data_fetcher.py
import yfinance as yf
from datetime import datetime

def get_stock_info(ticker_symbol="TSLA"):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return {
        "current_price": info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "market_cap": info.get("marketCap"),
        "beta": info.get("beta"),
        "symbol": ticker_symbol
    }

def get_option_expirations(ticker_symbol="TSLA"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.options  # returns a list of expiration dates

def get_put_option_chain(ticker_symbol="TSLA", expiration=None):
    ticker = yf.Ticker(ticker_symbol)
    if expiration is None:
        expiration = ticker.options[0]  # soonest expiry by default

    option_chain = ticker.option_chain(expiration)
    return option_chain.puts  # DataFrame

def get_historical_price(ticker_symbol="TSLA", period="5d"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period=period)
