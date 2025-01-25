import streamlit as st

def render(df):
    st.header('📌 Insights')
    st.subheader('Análise Quantitativa')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tendência MACD", 
                 "Alta" if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else "Baixa",
                 delta=f"{df['MACD'].iloc[-1] - df['Signal'].iloc[-1]:.2f}")
    
    with col2:
        st.metric("Suporte Técnico", 
                 f"${df['Lower_BB'].iloc[-1]:.2f}",
                 "Bollinger Lower")
    
    with col3:
        st.metric("Resistência Técnica", 
                 f"${df['Upper_BB'].iloc[-1]:.2f}",
                 "Bollinger Upper")
    
    st.divider()
    
    # Análise de Regime de Mercado
    volatility = df['Volatility'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    
    if volatility > 0.8:
        regime = "Mercado Altamente Volátil"
        recomendacao = "Considerar estratégias de curto prazo com stop loss rigoroso"
    elif rsi > 70:
        regime = "Condição de Sobrecompra"
        recomendacao = "Possível oportunidade de venda"
    elif rsi < 30:
        regime = "Condição de Sobrevenda"
        recomendacao = "Possível oportunidade de compra"
    else:
        regime = "Mercado em Tendência Neutra"
        recomendacao = "Manter posições existentes"
    
    st.subheader("Diagnóstico de Mercado")
    st.markdown(f"""
    **Regime Atual:** {regime}  
    **Recomendação:** {recomendacao}  
    **Fundamentação:**  
    - Volatilidade atual: {volatility*100:.1f}% (limiar > 80%)  
    - RSI atual: {rsi:.1f} (sobrecompra >70, sobrevenda <30)
    """)