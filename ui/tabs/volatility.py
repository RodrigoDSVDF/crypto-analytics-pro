import streamlit as st
import plotly.express as px

def render(df):
    st.header('🌡️ Volatilidade')
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x='timestamp', y='Volatility',
                     title='Volatilidade Histórica (30 dias)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(df, x='Volatility', 
                          title='Distribuição de Volatilidade',
                          nbins=50)
        st.plotly_chart(fig, use_container_width=True)