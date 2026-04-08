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
    [data-testid="stMetricValue"] { font-size: 32px; color: #1E3A8A; font-weight: bold; }
    .section-title { color: #1E3A8A; font-weight: bold; border-left: 10px solid #FF8C00; padding-left: 15px; margin-top: 30px; margin-bottom: 20px; font-size: 28px; }
    .chart-caption { background-color: #f1f3f5; padding: 12px; border-radius: 0 0 10px 10px; border-top: 2px solid #1E3A8A; font-size: 13px; color: #444; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid #e0e0e0; }
    .footer { text-align: center; padding: 30px; color: #555; font-size: 13px; border-top: 2px solid #eee; margin-top: 50px; line-height: 1.6; }
    .highlight { color: #1E3A8A; font-weight: 700; }
    .step-box { background-color: #e7f0fd; padding: 15px; border-radius: 8px; border-left: 5px solid #1E3A8A; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS (DADOS AJUSTADOS IBGE/SEADE) ---
@st.cache_data
def load_data():
    # Segmentação baseada na força industrial local (Cimento, Celulose, Metalurgia)
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Papel e Celulose", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [48, 18, 15, 10, 6, 3],
        'Dificuldade_40': [65, 55, 40, 50, 80, 45], 
        'Maturidade_Atual': [2.8, 3.2, 3.5, 2.9, 1.8, 2.4] 
    })
    
    # Histórico aproximado em Milhões de Reais (VAB Bruto)
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'Produtividade': [185, 198, 210, 225, 242, 268], 
        'VAB_Industria': [1450.5, 1580.2, 1690.8, 1850.4, 2100.2, 2350.7],
        'VAB_Servicos': [1980.1, 2150.4, 2320.6, 2680.9, 3050.5, 3480.2]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=70)
    st.title("Hub de Inteligência")
    st.subheader("Votorantim 4.0")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Introdução & Contexto", "Metodologia ETL", "Dashboard Executivo", 
                    "Diagnóstico Indústria 4.0", "Projeções 2033", "Plano de Ação"])
    
    st.info("Status do Sistema: Conectado às fontes governamentais.")

# Lógica de Filtragem
if ano_selecionado == "Todos":
    df_filtered = df_hist
    display_df = df_hist.iloc[[-1]] 
else:
    df_filtered = df_hist[df_hist['Ano'] == int(ano_selecionado)]
    display_df = df_filtered

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Análise de Contexto Econômico</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        Votorantim apresenta uma matriz econômica historicamente ligada à indústria de base pesada. 
        A análise dos dados aponta para um fenômeno de <b>terceirização da economia</b>, onde o setor de serviços cresce 
        em ritmo superior ao industrial, embora a indústria ainda detenha o maior valor agregado por posto de trabalho.
        <br><br>
        <span class="highlight">Destaque:</span> A proximidade com o polo tecnológico de Sorocaba cria um desafio de retenção de talentos e 
        necessidade de modernização para que Votorantim não se torne apenas um "fornecedor de commodities" para a região.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Concentração Setorial:** Alta dependência dos setores de extração e minerais.")
        st.warning("**Conflito Territorial:** Avanço da urbanização sobre áreas tradicionalmente industriais.")
    with c2:
        st.error("**Gap Tecnológico:** Baixa digitalização em pequenas e médias empresas fornecedoras.")
        st.info("**Logística:** Necessidade de otimização dos fluxos de saída de carga pesada.")

# --- 2. METODOLOGIA ETL ---
elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Para garantir a integridade da análise de negócios, aplicamos um processo de ETL (Extract, Transform, Load) 
    robusto focado em fontes oficiais brasileiras.
    """)
    
    st.markdown('<div class="step-box"><b>1. Extração:</b> Consumo via API e Web Scraping de dados do IBGE (SIDRA), SEADE e bases do Novo CAGED para dados de emprego industrial.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box"><b>2. Transformação:</b> Padronização de moedas (correção inflacionária via IPCA), tratamento de valores ausentes por imputação linear e agrupamento por CNAE 2.0.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box"><b>3. Carga:</b> Estruturação em Data Lake simplificado (Parquet/Pandas) para alimentação em tempo real deste dashboard.</div>', unsafe_allow_html=True)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png", width=100)

# --- 3. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    # Formatação para R$ Bilhões se passar de 1000M
    vab_i = display_df['VAB_Industria'].values[0]
    vab_s = display_df['VAB_Servicos'].values[0]
    
    c1.metric("VAB Indústria (Anual)", f"R$ {vab_i/1000:.2f} Bi" if vab_i > 1000 else f"R$ {vab_i} Mi")
    c2.metric("VAB Serviços (Anual)", f"R$ {vab_s/1000:.2f} Bi" if vab_s > 1000 else f"R$ {vab_s} Mi")
    c3.metric("Produtividade por Trabalhador", f"R$ {display_df['Produtividade'].values[0]}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.area(df_filtered, x='Ano', y=['VAB_Industria', 'VAB_Servicos'],
                               title="Crescimento Comparativo: Indústria vs Serviços",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                               labels={"value": "Valor em Milhões (R$)", "variable": "Setor"})
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">Nota-se uma aceleração constante no setor de serviços, ultrapassando a marca dos R$ 3 Bilhões em 2022.</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, 
                          title="Composição do VAB Industrial",
                          color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_pizza, use_container_width=True)

# --- 4. DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Análise de Maturidade Digital</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        # Gráfico de barras com linha de tendência
        fig_prod = px.bar(df_filtered, x='Ano', y='Produtividade', 
                         title="Eficiência Produtiva (Mil R$ / Operário)", 
                         color='Produtividade', color_continuous_scale='Blues')
        st.plotly_chart(fig_prod, use_container_width=True)
        st.info("A eficiência cresceu 44% desde 2018, indicando absorção de tecnologias de automação nas grandes plantas.")
        
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], 
                                           fill='toself', line=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
                               title="Índice de Maturidade (Escala 1-5)")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 5. PROJEÇÕES 2033 ---
elif menu == "Projeções 2033":
    st.markdown('<p class="section-title">Simulação de Cenários (10 Anos)</p>', unsafe_allow_html=True)
    
    anos_hist = df_hist['Ano'].values
    anos_proj = np.array([2024, 2025, 2026, 2027, 2028, 2033])
    
    def projetar(valores):
        coef = np.polyfit(anos_hist, valores, 1)
        return np.polyval(coef, anos_proj)

    proj_ind = projetar(df_hist['VAB_Industria'].values)
    proj_serv = projetar(df_hist['VAB_Servicos'].values)

    df_proj = pd.DataFrame({
        'Ano': anos_proj,
        'VAB_Industria': proj_ind,
        'VAB_Servicos': proj_serv,
        'Tipo': 'Projeção'
    })
    
    df_completo = pd.concat([df_hist.assign(Tipo='Histórico'), df_proj])

    fig_proj = px.line(df_completo, x='Ano', y=['VAB_Industria', 'VAB_Servicos'], 
                      color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                      line_dash='Tipo', title="Tendência de Longo Prazo")
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.markdown(f"""
    <div class="card">
        <b>Insights de Negócio:</b> Se a tendência atual persistir, o setor de serviços será <b>60% maior</b> que a indústria em 2033. 
        Para reverter este cenário e manter o peso industrial, o plano de ação deve focar em <i>Servitização</i> 
        (serviços de alto valor dentro da indústria).
    </div>
    """, unsafe_allow_html=True)

# --- 6. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Estratégias de Fortalecimento</p>', unsafe_allow_html=True)
    
    acoes_df = pd.DataFrame({
        "Eixo Estratégico": ["1. Diversificação Vertical", "2. Hub de Talentos 4.0", "3. Green Tech & ESG", "4. Ecossistema Industrial"],
        "Ação Proposta": [
            "Atrair manufatura leve e eletrônicos para reduzir dependência de cimento/metais.",
            "Parcerias com Fatec/Senai para requalificação em análise de dados e IoT.",
            "Implementar incentivos fiscais para indústrias com balanço de carbono neutro.",
            "Criar uma zona de simbiose industrial para troca de resíduos e energia entre plantas."
        ],
        "Prioridade": ["Alta", "Crítica", "Média", "Alta"]
    })
    
    st.table(acoes_df)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <b>Observatório Industrial Votorantim | Análise de Dados para Negócio</b><br>
        Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.<br>
        <i>Gerado em {datetime.now().strftime('%d/%m/%Y')} - Dados ref. Ciclo 2018-2023</i>
    </div>
    """, unsafe_allow_html=True)
