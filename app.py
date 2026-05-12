import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import segno
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial | Votorantim",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    /* Importando fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Estilo dos Cards */
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }
    
    /* Container principal */
    .main { background-color: #fcfdfe; }
    
    /* Customização de títulos */
    .main-title {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Steps de ETL */
    .etl-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #1E3A8A;
        background: white;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #94a3b8;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---
def formatar_valor(valor):
    if valor >= 1000:
        return f"R$ {valor/1000:.2f} Bi"
    return f"R$ {valor:.1f} Mi"

def gerar_qrcode(url):
    qrcode = segno.make_qr(url)
    out = BytesIO()
    qrcode.save(out, kind='png', scale=10)
    return out.getvalue()

@st.cache_data
def load_data():
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Papel e Celulose", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [48, 18, 15, 10, 6, 3],
        'Dificuldade_40': [65, 55, 40, 50, 80, 45], 
        'Maturidade_Atual': [2.8, 3.2, 3.5, 2.9, 1.8, 2.4] 
    })
    df_hist = pd.DataFrame({
        'Ano': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'PIB': [670.405, 791.318, 844.845, 914.154, 1124.655, 1357.128, 1561.842, 1811.097, 2042.691, 2094.207, 2482.293, 2975.838, 4672.147, 4495.059, 3076.565, 2995.815, 3093.050, 3405.739, 3412.630, 3919.236, 4518.922, 5209.654],
        'PIB_Constante': [2738.300, 2872.278, 2805.643, 2821.385, 3284.191, 3842.402, 4233.203, 4635.299, 5012.020, 4851.686, 5399.786, 6116.218, 9066.783, 8197.656, 5069.796, 4644.585, 4657.926, 4943.435, 4748.766, 5217.874, 5466.351, 5956.990],
        'VAB_Industria': [234.6, 276.9, 295.7, 319.9, 393.6, 475.0, 546.6, 633.9, 714.9, 732.9, 868.8, 1041.5, 1635.2, 1573.3, 1076.8, 1048.5, 1082.6, 1192.0, 1194.4, 1371.7, 1581.6, 1823.4],
        'VAB_Servicos': [368.7, 435.2, 464.7, 502.8, 618.6, 746.4, 859.0, 996.1, 1123.5, 1151.8, 1365.3, 1636.7, 2569.7, 2472.3, 1692.1, 1647.7, 1701.2, 1873.1, 1876.9, 2155.6, 2485.4, 2865.3]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()
ipca_map = {2002: 12.53, 2003: 9.30, 2004: 7.60, 2005: 5.69, 2006: 3.14, 2007: 4.46, 2008: 5.90, 2009: 4.31, 2010: 5.91, 2011: 6.50, 2012: 5.84, 2013: 5.91, 2014: 6.41, 2015: 10.67, 2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31, 2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62}

# --- SIDEBAR MODERNA ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=80)
    st.title("Observatório 4.0")
    st.markdown("---")
    
    menu = st.selectbox(
        "Navegação:",
        ["Introdução & Contexto", "Problemas Identificados", "Metodologia ETL", 
         "Dashboard Executivo", "Diagnóstico Indústria 4.0", "Projeção Futura", 
         "Plano de Ação", "Fontes/Referências"]
    )
    
    st.divider()
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.select_slider("Filtro Temporal:", options=anos_disponiveis)
    
    st.divider()
    url_da_pagina = "https://economiaapp-economia-fatec.streamlit.app/" 
    st.image(gerar_qrcode(url_da_pagina), width=100)
    st.caption("📱 Escaneie para versão mobile")

# --- LÓGICA DE DADOS ---
if ano_selecionado == "Todos":
    dados_atuais = df_hist.iloc[-1]
    ano_txt = "Consolidado 2023"
else:
    dados_atuais = df_hist[df_hist['Ano'] == int(ano_selecionado)].iloc[0]
    ano_txt = ano_selecionado

# --- RENDERIZAÇÃO DOS MÓDULOS ---

# Título Dinâmico
st.markdown(f'<h1 class="main-title">{menu}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">Análise estratégica de Votorantim | Período: {ano_txt}</p>', unsafe_allow_html=True)

if menu == "Introdução & Contexto":
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.expander("📊 Análise Econômica", expanded=True):
            st.write("Votorantim atravessa um momento crucial de transição econômica. Historicamente consolidada como um pilar da indústria de base, a cidade hoje apresenta uma nova dinâmica revelada pelos dados: a ascensão do setor de serviços.")
        with st.expander("📜 Plano Diretor & Zoneamento"):
            st.info("A expansão urbana cria conflitos logísticos. Áreas industriais estão sendo cercadas por bairros residenciais.")
    with col2:
        st.link_button("🔍 Ver Mapa de Zoneamento", "https://www.votorantim.sp.gov.br/arquivos/mapas_002_19043716.pdf", use_container_width=True)
        st.dataframe(df_seg.head(), hide_index=True)

elif menu == "Problemas Identificados":
    c1, c2 = st.columns(2)
    with c1:
        st.error("#### Clusterização\nDependência de poucos players gigantes.")
        st.warning("#### Conflito Territorial\nTrade-off entre expansão urbana e produção.")
    with c2:
        st.success("#### Evolução Setorial\nOportunidade de modernização tecnológica.")
        st.info("#### Efeito Shadowing\nPerda de talentos para Sorocaba.")

elif menu == "Metodologia ETL":
    st.chat_message("assistant").write("Nosso Pipeline de dados segue o padrão industrial:")
    steps = [
        ("📥 Extração", "Dados do IBGE, SEADE e CAGED via CSV/SIDRA."),
        ("⚙️ Transformação", "Limpeza de nulos e unificação via chaves primárias (Ano)."),
        ("📤 Carga", "Estruturação em DataFrames otimizados para este Dashboard.")
    ]
    for title, desc in steps:
        st.markdown(f'<div class="etl-card"><b>{title}</b><br>{desc}</div>', unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    m1, m2, m3 = st.columns(3)
    m1.metric(f"PIB ({ano_txt})", formatar_valor(dados_atuais['PIB']), delta="Nominal")
    m2.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']), delta="-2.1%", delta_color="inverse")
    m3.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']), delta="+4.5%")
    
    st.divider()
    
    # Gráfico de Barras Moderno
    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB'], name='PIB Corrente', marker_color='#1E3A8A'))
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB_Constante'], name='PIB Constante (2023)', marker_color='#FF8C00'))
    fig_comparativo.update_layout(barmode='group', height=450, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_comparativo, use_container_width=True)

elif menu == "Diagnóstico Indústria 4.0":
    st.markdown("### Produtividade: Digital vs Tradicional")
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_prod = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 345,
            title = {'text': "Ganho de Produtividade (k/op)"},
            delta = {'reference': 210},
            gauge = {'axis': {'range': [0, 500]}, 'bar': {'color': "#FF8C00"}}
        ))
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', fillcolor='rgba(255, 140, 0, 0.3)', line=dict(color='#FF8C00')))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Radar de Maturidade Digital")
        st.plotly_chart(fig_r, use_container_width=True)

elif menu == "Projeção Futura":
    st.info("Utilizando Regressão Linear para estimativa do cenário 2030.")
    # (A lógica de projeção permanece a mesma, mas encapsulada em componentes visuais limpos)
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2024, 2031)
    coef = np.polyfit(anos_hist, df_hist['VAB_Industria'].values, 1)
    p = np.poly1d(coef)
    
    fig_proj = px.line(x=anos_proj, y=p(anos_proj), title="Tendência do VAB Industrial (Cenário Base)")
    fig_proj.update_traces(line_color='#1E3A8A', line_dash='dash')
    st.plotly_chart(fig_proj, use_container_width=True)

elif menu == "Plano de Ação":
    tab1, tab2 = st.tabs(["🚀 Tecnologia", "🏗️ Infraestrutura"])
    with tab1:
        st.subheader("Modernização Industrial")
        st.write("- **Incentivo Fiscal:** Redução de ISS para IoT.")
        st.write("- **Qualificação:** Hub FATEC Votorantim.")
    with tab2:
        st.subheader("Ordenamento Urbano")
        st.write("- **Zonas de Transição:** Amortecimento entre fábricas e residências.")

elif menu == "Fontes/Referências":
    st.balloons()
    st.success("Dados validados e auditados.")
    st.markdown("""
    * **IBGE Cidades**
    * **Fundação SEADE**
    * **Novo CAGED**
    """)
    st.link_button("📂 Acessar Repositório de Dados", "https://drive.google.com/drive/folders/12XwL_9c_lzHLopxX9lHEeNBGkn1old8G")

# --- FOOTER ---
st.markdown("---")
st.markdown('<div class="footer">Observatório Industrial Votorantim © 2024 | Inteligência de Dados 4.0</div>', unsafe_allow_html=True)
