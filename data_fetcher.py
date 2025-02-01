import ccxt
import pandas as pd
import streamlit as st
import os

# Configuração da Exchange (substitua pela escolhida)
def get_exchange():
    return ccxt.kraken({
        'enableRateLimit': True,  # Evita bloqueios por limite de requests
        # 'apiKey': os.getenv('KRAKEN_API_KEY'),  # Opcional (dados públicos não exigem)
        # 'secret': os.getenv('KRAKEN_SECRET_KEY'),
    })

@st.cache_data(ttl=300)
def fetch_crypto_data(symbol, timeframe='1d', limit=500):
    exchange = get_exchange()
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
    exchange = get_exchange()
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