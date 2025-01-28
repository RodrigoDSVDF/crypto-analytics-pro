import ccxt
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)  # Mantém o cache por 5 minutos
def fetch_crypto_data(symbol, timeframe='1d', limit=500):
    exchange = ccxt.binance({
        'apiKey': 'i4QeU6dT1xo2kKQYDnw3tqr5VATR4DcdEt3l6dInrmM9pfv9IHPczv7CGDRPZDTi',  # Use variáveis de ambiente!
        'secret': 'Mt1LVBB2N8hTgFIKmG50uwGKUxIYgiejhwJr8ozHw5xvhMJDC6bu4kq6iIdS5943',
    })
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df
    except Exception as e:
        st.error(f"Erro na API: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def fetch_order_book(symbol, limit=100):
    exchange = ccxt.binance()
    try:
        return exchange.fetch_order_book(symbol, limit=limit)
    except Exception as e:
        st.error(f"Erro no order book: {str(e)}")
        return None 