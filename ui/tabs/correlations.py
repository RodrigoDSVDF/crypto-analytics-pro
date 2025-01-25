import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import fetch_crypto_data
from config import CRYPTO_LIST

def render(selected_crypto, timeframe, main_df):
    st.header('🔗 Correlações')
    
    correlation_data = []
    for crypto in CRYPTO_LIST:
        if crypto != selected_crypto:
            temp_df = fetch_crypto_data(crypto, timeframe)
            if not temp_df.empty:
                correlation = main_df['close'].corr(temp_df['close'])
                correlation_data.append({'Moeda': crypto, 'Correlação': correlation})
    
    if correlation_data:
        corr_df = pd.DataFrame(correlation_data)
        fig = px.bar(corr_df.sort_values('Correlação'), 
                    x='Correlação', y='Moeda',
                    title=f'Correlação com {selected_crypto}',
                    color='Correlação',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
