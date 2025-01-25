import streamlit as st
from config import CRYPTO_LIST, TIMEFRAME_OPTIONS

def get_sidebar_selections():
    st.sidebar.title("Configurações")
    selected_crypto = st.sidebar.selectbox('Selecione a Criptomoeda', CRYPTO_LIST)
    timeframe = st.sidebar.selectbox('Período', TIMEFRAME_OPTIONS, index=1)
    return selected_crypto, timeframe