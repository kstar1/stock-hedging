import yfinance as yf
import streamlit as st

@st.cache_data
def get_option_expirations(ticker_symbol="TSLA"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.options  # returns a list of expiration dates

@st.cache_data
def get_put_option_chain(ticker_symbol="TSLA", expiration=None):
    ticker = yf.Ticker(ticker_symbol)
    if expiration is None:
        expiration = ticker.options[0]

    opt_chain = ticker.option_chain(expiration)
    return opt_chain.puts  # ✅ this is the missing line
