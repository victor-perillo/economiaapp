import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="Análise Industrial Votorantim", layout="wide")

# --- DATASET PREPARATION (Baseado no ETL do trabalho) ---
@st.cache_data
def load_data():
    # Dados de Participação (Página 4)
    df_vab = pd.DataFrame({
        'Segmento': ['Minerais Não Metálicos', 'Metalurgia', 'Química/Plásticos', 'Alimentos', 'Outros'],
        'Participacao': [55, 20, 12, 8, 5]
    })
    
    # Dados de Evolução (Página 5)
    df_evolucao = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021],
        'Indústria': [1520, 1610, 1740, 1920],
        'Serviços': [2100, 2250, 2380, 2750]
    })

    # Dados de Emprego (Página 5)
    df_emprego = pd.DataFrame({
        'Ano': [2019, 2020, 2021, 2022, 2023],
        'Estoque': [8450, 8120, 8600, 8750, 8920]
    })
    return df_vab, df_evolucao, df_emprego

df_vab, df_evolucao, df_emprego = load_data()

# --- SIDEBAR (Navegação) ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["Cenário Econômico", "Análise de Setores", "Indústria 4.0 & Plano de Ação"])

# --- PAGE 1: CENÁRIO ECONÔMICO ---
if page == "Cenário Econômico":
    st.title("📊 Cenário Econômico de Votorantim/SP")
    st.markdown("""Votorantim vive um processo de **transição de matriz econômica**, saindo do legacy industrial de base para um polo de serviços.""")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evolução do VAB (R$ Milhões)")
        fig_pib = px.bar(df_evolucao, x='Ano', y=['Indústria', 'Serviços'], barmode='group',
                         color_discrete_map={'Indústria': '#003f5c', 'Serviços': '#ffa600'})
        st.plotly_chart(fig_pib, use_container_width=True)
        st.info("Insight: O setor de Serviços acelera mais rápido que a Indústria (terceirização).")

    with col2:
        st.subheader("Estoque de Emprego Industrial")
        fig_emp = px.line(df_emprego, x='Ano', y='Estoque', markers=True, line_shape='linear',
                          color_discrete_sequence=['#2ca02c'])
        st.plotly_chart(fig_emp, use_container_width=True)
        st.success("Resiliência: Recuperação total dos postos de trabalho pós-pandemia (2020).")

# --- PAGE 2: ANÁLISE DE SETORES ---
elif page == "Análise de Setores":
    st.title("🏗️ Concentração e Dominância Industrial")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Maior Setor", "Minerais Não Metálicos", "55% do Share")
        st.warning("⚠️ Risco de Setor Único detectado.")
        st.write("**Problemas Identificados:**")
        st.write("- Dependência de poucos players gigantes.")
        st.write("- Skill Gap (Mão de Obra).")
        st.write("- Conflito de Zoneamento Urbano.")

    with col2:
        fig_tree = px.treemap(df_vab, path=['Segmento'], values='Participacao',
                              color='Participacao', color_continuous_scale='Blues',
                              title="Market Share Industrial (VAB %)")
        st.plotly_chart(fig_tree, use_container_width=True)

# --- PAGE 3: INDÚSTRIA 4.0 & PLANO DE AÇÃO ---
elif page == "Indústria 4.0 & Plano de Ação":
    st.title("💡 Inovação e Estratégia")
    
    st.subheader("Diagnóstico Indústria 4.0")
    st.write("A eficiência cresce acima da contratação, indicando automação e uso de IoT.")
    
    st.subheader("Plano de Ação Proposto")
    acoes = pd.DataFrame({
        "Ação": ["Diversificação Vertical", "Hub de Dados Regional", "Green Tech Incentives"],
        "Objetivo": ["Atrair manufatura leve (pré-moldados tech)", "Requalificar operários em IA (Parceria Sorocaba)", "Subsídios para energia limpa"],
        "Base de Dados": ["Treemap de Share", "Produtividade", "VAB Industrial"]
    })
    st.table(acoes)

    # Gráfico de Meta
    st.subheader("Estratégia de Diversificação: Meta de Portfólio")
    fig_meta = go.Figure(data=[
        go.Bar(name='Cenário Atual', x=['Cimento', 'Metais', 'Novas Techs'], y=[55, 20, 5], marker_color='#003f5c'),
        go.Bar(name='Meta Plano', x=['Cimento', 'Metais', 'Novas Techs'], y=[40, 20, 25], marker_color='#ffa600')
    ])
    st.plotly_chart(fig_meta, use_container_width=True)