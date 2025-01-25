import streamlit as st
import plotly.graph_objects as go

def render(df):
    st.header('📈 Análise Técnica')
    col1, col2 = st.columns([3,1])
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['MA20'], name='MA20', line=dict(color='orange', width=1)))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Upper_BB'], name='Bollinger Upper', 
                               line=dict(color='gray', width=1, dash='dot')))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Lower_BB'], name='Bollinger Lower',
                               line=dict(color='gray', width=1, dash='dot')))
        fig.update_layout(height=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader('Indicadores Chave')
        st.metric("Preço Atual", f"${df['close'].iloc[-1]:.2f}")
        st.metric("Volume 24h", f"${df['volume'].iloc[-1]:,.0f}")
        st.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.1f}")
        st.metric("Volatilidade Anualizada", f"{df['Volatility'].iloc[-1]*100:.1f}%")