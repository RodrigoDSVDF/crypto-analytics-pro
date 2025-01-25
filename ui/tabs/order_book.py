import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_fetcher import fetch_order_book

def render(selected_crypto):
    st.header('📊 Livro de Ofertas')
    st.markdown("""
    O **Livro de Ofertas** apresenta o volume de ordens de compra e venda para a criptomoeda selecionada, 
    permitindo visualizar o comportamento de mercado em tempo real.
    """)

    order_book = fetch_order_book(selected_crypto)
    
    if order_book.empty:
        st.warning("Não há dados disponíveis para a criptomoeda selecionada. Por favor, escolha outra.")
        return
    
    # Resumo
    total_asks = order_book['asks'].sum()
    total_bids = order_book['bids'].sum()
    st.subheader(f"Resumo - {selected_crypto}")
    st.write(f"- **Volume total de vendas (asks):** {total_asks:,.2f}")
    st.write(f"- **Volume total de compras (bids):** {total_bids:,.2f}")

    # Configuração de cores
    st.sidebar.header("Configurações de Cores")
    ask_color = st.sidebar.color_picker("Cor para Ordens de Venda", "#FF0000")
    bid_color = st.sidebar.color_picker("Cor para Ordens de Compra", "#00FF00")
    
    # Layout responsivo
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gráfico de Barras - Volume por Preço")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=order_book['asks'],
            y=order_book['price'],
            name='Ordens de Venda',
            orientation='h',
            marker_color=ask_color
        ))
        fig.add_trace(go.Bar(
            x=order_book['bids'],
            y=order_book['price'],
            name='Ordens de Compra',
            orientation='h',
            marker_color=bid_color
        ))
        fig.update_layout(
            height=500, 
            xaxis_title='Volume', 
            yaxis_title='Preço',
            legend_title='Tipo de Ordem',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Gráfico de Linhas - Distribuição de Ordens")
        fig = px.line(
            order_book, 
            x='price', 
            y=['asks', 'bids'], 
            title='Distribuição de Ordens',
            labels={'price': 'Preço', 'value': 'Volume', 'variable': 'Tipo de Ordem'},
            color_discrete_map={'asks': ask_color, 'bids': bid_color}
        )
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
