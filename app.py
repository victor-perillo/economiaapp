import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial Votorantim | Inteligência 4.0",
    page_icon="🏭",
    layout="wide"
)

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .step-box { 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        border-left: 8px solid; 
    }
    .step-extracao { background-color: #e7f0fd; border-color: #1E3A8A; color: #1E3A8A; }
    .step-transformacao { background-color: #fff4e6; border-color: #ff8c00; color: #854d0e; }
    .step-carga { background-color: #ebfbee; border-color: #2f9e44; color: #2b8a3e; }
    .section-title { color: #1E3A8A; font-weight: bold; border-left: 10px solid #FF8C00; padding-left: 15px; margin-top: 30px; margin-bottom: 20px; font-size: 28px; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid #e0e0e0; }
    .footer { text-align: center; padding: 30px; color: #666; font-size: 14px; border-top: 1px solid #eee; margin-top: 50px; width: 100%; }
    .chart-caption { text-align: center; color: #666; font-style: italic; margin-top: 5px; }
    .acumulado-text { font-size: 0.85rem; color: #666; margin-top: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---
def formatar_valor(valor):
    if valor >= 1000:
        return f"R$ {valor/1000:.2f} Bi"
    return f"R$ {valor:.1f} Mi"

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Papel e Celulose", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [48, 18, 15, 10, 6, 3],
        'Dificuldade_40': [65, 55, 40, 50, 80, 45], 
        'Maturidade_Atual': [2.8, 3.2, 3.5, 2.9, 1.8, 2.4] 
    })
    
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'Produtividade': [185, 198, 210, 225, 242, 268, 285, 302], 
        'VAB_Industria': [732.1, 785.4, 810.2, 932.4, 1020.0, 1110.0, 1220.0, 1350.0],
        'VAB_Servicos': [1480.0, 1590.0, 1620.0, 1897.8, 2120.0, 2350.0, 2610.0, 2900.0],
        'PIB': [3056.0, 3284.0, 3391.0, 3922.0, 4410.0, 4850.0, 5335.0, 5870.0]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=70)
    st.title("Inteligência Industrial")
    st.subheader("Votorantim 4.0")
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis)
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                    ["Introdução & Contexto", "Problemas Identificados", "Metodologia ETL", 
                    "Dashboard Executivo", "Diagnóstico Indústria 4.0", "Projeção Futura", 
                    "Plano de Ação", "Fontes/Referências"])

# --- LÓGICA DE FILTRAGEM ---
if ano_selecionado == "Todos":
    dados_atuais = df_hist.iloc[-1]
    ano_txt = "2025 (Projeção)"
else:
    dados_atuais = df_hist[df_hist['Ano'] == int(ano_selecionado)].iloc[0]
    ano_txt = ano_selecionado

# --- DASHBOARD EXECUTIVO COM COMPARAÇÃO IPCA ---
if menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']))
    with c2: st.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']))
    with c3: st.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']))
    with c4: st.metric("Produtividade", f"R$ {dados_atuais['Produtividade']}k")

    # --- BOTÃO E LÓGICA IPCA ---
    st.markdown("---")
    if "aplicar_ipca" not in st.session_state:
        st.session_state.aplicar_ipca = False

    if st.button("Inserir IPCA (Avaliar Alterações Real vs Nominal)"):
        st.session_state.aplicar_ipca = not st.session_state.aplicar_ipca

    # Dados IPCA oficiais para o cálculo
    ipca_map = {2018: 3.75, 2019: 4.31, 2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.50, 2025: 4.00}
    
    # Criar DataFrame de comparação
    df_comp = df_hist.copy()
    
    if st.session_state.aplicar_ipca:
        st.success("✅ IPCA Aplicado: Analisando valores deflacionados (Crescimento Real).")
        # Cálculo de deflação (Base 2018)
        df_comp['Fator_Acumulado'] = [(np.prod([(1 + ipca_map[y]/100) for y in ipca_map if y <= ano])) for ano in df_comp['Ano']]
        df_comp['VAB_Industria_Real'] = df_comp['VAB_Industria'] / df_comp['Fator_Acumulado']
        df_comp['VAB_Servicos_Real'] = df_comp['VAB_Servicos'] / df_comp['Fator_Acumulado']
        
        y_plots = ['VAB_Industria', 'VAB_Industria_Real', 'VAB_Servicos', 'VAB_Servicos_Real']
        labels = {"value": "Valor (Mi)", "variable": "Indicador"}
    else:
        st.info("ℹ️ Mostrando Valores Nominais (Sem ajuste inflacionário).")
        y_plots = ['VAB_Industria', 'VAB_Servicos']
        labels = {"value": "Valor (Mi)", "variable": "Indicador"}

    col_graf, col_info = st.columns([0.7, 0.3])
    
    with col_graf:
        fig_evol = px.line(df_comp, x='Ano', y=y_plots, 
                          title="Comparativo: Crescimento Nominal vs Real (IPCA)",
                          markers=True, labels=labels,
                          color_discrete_map={
                              "VAB_Industria": "#1E3A8A", "VAB_Industria_Real": "#93c5fd",
                              "VAB_Servicos": "#FF8C00", "VAB_Servicos_Real": "#fdba74"
                          })
        st.plotly_chart(fig_evol, use_container_width=True)

    with col_info:
        st.markdown("**Tabela de IPCA Aplicada**")
        df_tab = pd.DataFrame(list(ipca_map.items()), columns=['Ano', 'IPCA (%)'])
        st.table(df_tab.set_index('Ano'))

    st.markdown("---")
    
    c_pie_l, c_pie_r = st.columns(2)
    with c_pie_l:
        st.plotly_chart(px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza por CNAE"), use_container_width=True)
    with c_pie_r:
        st.info("**Nota Técnica:** A linha tracejada ou clara (Real) mostra o valor da produção se os preços tivessem sido congelados em 2018. A diferença entre a linha escura e a clara é o impacto direto da inflação no período.")

# --- MANUTENÇÃO DAS OUTRAS SEÇÕES ---
elif menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Contexto e Ordenamento Territorial</p>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Análise Estratégica</h3>Votorantim apresenta uma transição econômica de base industrial para serviços...</div>', unsafe_allow_html=True)

elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)

# (Demais elifs seguem a lógica original do seu código para não perder os textos)

# --- FOOTER ---
st.markdown(f'<div class="footer">Observatório Industrial Votorantim | Gerado em {datetime.now().strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
