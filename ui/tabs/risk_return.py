import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import fetch_crypto_data
from technical_analysis import calculate_risk_return
from config import CRYPTO_LIST

def render(timeframe):
    st.header('📉 Risco-Retorno')
    
    risk_return_data = []
    for crypto in CRYPTO_LIST:
        temp_df = fetch_crypto_data(crypto, timeframe)
        if not temp_df.empty:
            temp_df = calculate_risk_return(temp_df)
            risk_return_data.append({
                'Moeda': crypto,
                'Retorno': temp_df['Return'].mean() * 365,
                'Risco': temp_df['Risk'].mean()
            })
    
    if risk_return_data:
        risk_return_df = pd.DataFrame(risk_return_data)
        fig = px.scatter(risk_return_df, x='Risco', y='Retorno', text='Moeda',
                        title='Risco-Retorno das Criptomoedas',
                        color='Retorno', color_continuous_scale='RdYlGn')
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)