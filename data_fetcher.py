import ccxt
import pandas as pd
import streamlit as st
import os

# Configuração dinâmica da exchange (Binance vs. Binance US)
def get_exchange():
    # Use Binance US em produção (se aplicável)
    if os.getenv('ENVIRONMENT') == 'production':
        return ccxt.binanceus({'enableRateLimit': True})
    else:
        return ccxt.binance({'enableRateLimit': True})

@st.cache_data(ttl=300)
def fetch_crypto_data(symbol, timeframe='1d', limit=500):
    exchange = get_exchange()  # Chama a configuração dinâmica
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['symbol'] = symbol
        return df
    except ccxt.NetworkError as e:
        st.error(f"Erro de rede (Binance API bloqueada?): {str(e)}")
        st.markdown("""
            **Solução:** 
            - Se o servidor está nos EUA, use [Binance US](https://www.binance.us).
            - Verifique a região do servidor de produção.
        """)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao coletar dados para {symbol}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def fetch_order_book(symbol, limit=100):
    exchange = get_exchange()  # Chama a configuração dinâmica
    try:
        order_book = exchange.fetch_order_book(symbol, limit=limit)
        return pd.DataFrame({
            'price': order_book['asks'][0][0],
            'asks': [ask[1] for ask in order_book['asks']],
            'bids': [bid[1] for bid in order_book['bids']]
        })
    except ccxt.NetworkError as e:
        st.error(f"Erro 451: Binance bloqueou o acesso do servidor. Detalhes: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro no order book para {symbol}: {str(e)}")
        return pd.DataFrame()