import yfinance as yf
import streamlit as st
from datetime import datetime

@st.cache_data
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

@st.cache_data
def get_historical_price(ticker_symbol="TSLA", period="5d"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period=period)