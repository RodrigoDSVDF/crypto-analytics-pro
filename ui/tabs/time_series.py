import streamlit as st
import plotly.express as px


def render(df):
    st.header('📅 Série Temporal')
    
    # Adiciona opção de seleção de médias móveis
    ma_periods = st.multiselect('Selecione Médias Móveis:', 
                               [20, 50, 200],
                               default=[20, 200])
    
    fig = px.line(df, 
                 x='timestamp', 
                 y='close',
                 title=f'Evolução do Preço - {df["symbol"].iloc[0]}',
                 labels={'close': 'Preço (USDT)', 'timestamp': 'Data'})
    
    # Adiciona as médias móveis selecionadas
    for period in ma_periods:
        ma_column = f'MA{period}'
        if ma_column in df.columns:
            fig.add_scatter(x=df['timestamp'], 
                           y=df[ma_column],
                           name=f'MA{period}',
                           line=dict(width=1))
    
    fig.update_layout(
        hovermode='x unified',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    