import streamlit as st
from src.ui.tabs.put_chain_tab import render_put_chain_tab

# You’ll also need to manually set up session state variables
st.session_state.ticker = "TSLA"
st.session_state.stock_info = {"current_price": 180}
st.session_state.selected_expiration = "2024-12-20"

render_put_chain_tab()
