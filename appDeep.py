import streamlit as st
import pandas as pd
from datetime import datetime
from data_fetcher import fetch_crypto_data
from technical_analysis import calculate_technical_indicators, calculate_risk_return
from ui.sidebar import get_sidebar_selections
from ui.tabs import (
    time_series,
    technical_analysis, 
    order_book, 
    volatility, 
    correlations, 
    insights, 
    risk_return
)

# Configuração da página
st.set_page_config(page_title='Crypto Analytics Pro', layout='wide')

# JavaScript para recarregar a página a cada 60 segundos
st.components.v1.html(
    """
    <script>
    function reloadPage() {
        setTimeout(function() {
            window.location.reload();
        }, 60000);  // 60 segundos
    }
    reloadPage();
    </script>
    """
)

# Header principal
st.title('Análise Profissional de Criptomoedas')
st.markdown("""
**Plataforma de Análise Técnica Avançada**  
Dados em tempo real via Binance API • Atualização contínua
""")

# Sidebar
selected_crypto, timeframe = get_sidebar_selections()

# Controle da última atualização
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now().strftime('%H:%M:%S')

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Última atualização:** {st.session_state.last_update}")
st.sidebar.markdown("Dados atualizados a cada 5 minutos ⏱️")

# Carregamento de dados principal
df = fetch_crypto_data(selected_crypto, timeframe)
if not df.empty:
    df = calculate_technical_indicators(df)
    df = calculate_risk_return(df)
    # Atualiza o timestamp
    st.session_state.last_update = datetime.now().strftime('%H:%M:%S')
else:
    st.error("Falha ao carregar dados principais")
    st.stop()

# Criação das abas
tabs = st.tabs([
    '📅 Série Temporal',
    '📈 Análise Técnica', 
    '📊 Order Book', 
    '🌡️ Volatilidade', 
    '🔗 Correlações',
    '📌 Insights',
    '📉 Risco-Retorno'
])

# Renderização das abas
with tabs[0]:
    time_series.render(df)

with tabs[1]:
    technical_analysis.render(df)

with tabs[2]:
    order_book.render(selected_crypto)

with tabs[3]:
    volatility.render(df)

with tabs[4]:
    correlations.render(selected_crypto, timeframe, df)

with tabs[5]:
    insights.render(df)

with tabs[6]:
    risk_return.render(timeframe)