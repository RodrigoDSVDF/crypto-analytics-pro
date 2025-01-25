import ccxt
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def fetch_crypto_data(symbol, timeframe='1d', limit=500):
    exchange = ccxt.binance()
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df
    except Exception as e:
        st.error(f"Erro ao coletar dados para {symbol}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def fetch_order_book(symbol, limit=100):
    exchange = ccxt.binance()
    try:
        order_book = exchange.fetch_order_book(symbol, limit=limit)
        return pd.DataFrame({
            'price': order_book['asks'][0][0],
            'asks': [ask[1] for ask in order_book['asks']],
            'bids': [bid[1] for bid in order_book['bids']]
        })
    except Exception as e:
        st.error(f"Erro no order book para {symbol}: {str(e)}")
        return pd.DataFrame()