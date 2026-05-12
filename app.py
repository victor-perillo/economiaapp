import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import segno
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Votorantim 4.0",
    page_icon="🏭",
    layout="wide"
)

# --- SISTEMA DE DESIGN (CSS AVANÇADO) ---
st.markdown("""
    <style>
    /* Fundo e Container Principal */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Estilização dos Cards Brancos */
    div[data-testid="stVerticalBlock"] > div:has(div.card-bi) {
        background-color: transparent !important;
    }
    
    .card-bi {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
    }

    /* Títulos e Seções */
    .section-header {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 800;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 5px;
        margin-bottom: 20px;
    }
    
    /* Steps de ETL Estilizados */
    .etl-step {
        background: #ffffff;
        border-left: 6px solid #3b82f6;
        padding: 1rem;
        margin: 10px 0;
        border-radius: 4px 10px 10px 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* Customização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #3b82f6;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES SUPORTE ---
def formatar_valor(valor):
    if valor >= 1000: return f"R$ {valor/1000:.2f} Bi"
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
        'Ano': list(range(2002, 2024)),
        'PIB': [670.405, 791.318, 844.845, 914.154, 1124.655, 1357.128, 1561.842, 1811.097, 2042.691, 2094.207, 2482.293, 2975.838, 4672.147, 4495.059, 3076.565, 2995.815, 3093.050, 3405.739, 3412.630, 3919.236, 4518.922, 5209.654],
        'VAB_Industria': [234.6, 276.9, 295.7, 319.9, 393.6, 475.0, 546.6, 633.9, 714.9, 732.9, 868.8, 1041.5, 1635.2, 1573.3, 1076.8, 1048.5, 1082.6, 1192.0, 1194.4, 1371.7, 1581.6, 1823.4],
        'VAB_Servicos': [368.7, 435.2, 464.7, 502.8, 618.6, 746.4, 859.0, 996.1, 1123.5, 1151.8, 1365.3, 1636.7, 2569.7, 2472.3, 1692.1, 1647.7, 1701.2, 1873.1, 1876.9, 2155.6, 2485.4, 2865.3]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR E NAVEGAÇÃO ---
with st.sidebar:
    st.markdown("### 🏭 INTELIGÊNCIA 4.0")
    menu = st.radio("Módulos Estratégicos", 
                    ["Home & Contexto", "Análise de Problemas", "Pipeline de Dados", 
                     "Dashboard Executivo", "Diagnóstico 4.0", "Plano de Ação"],
                    index=0)
    
    st.markdown("---")
    ano_sel = st.select_slider("Filtro de Histórico", options=df_hist['Ano'].tolist(), value=2023)
    
    st.markdown("---")
    qr_img = gerar_qrcode("https://economiaapp-economia-fatec.streamlit.app/")
    st.image(qr_img, caption="Acesse o App", width=120)

# --- LÓGICA DE FILTRO ---
dados_atuais = df_hist[df_hist['Ano'] == ano_sel].iloc[0]

# --- RENDERIZAÇÃO DOS MÓDULOS ---

if menu == "Home & Contexto":
    st.markdown('<h1 class="section-header">Observatório Industrial Votorantim</h1>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div class="card-bi">
            <h3>Visão Geral do Município</h3>
            <p>Votorantim vive uma transição entre sua base histórica de mineração e a ascensão do setor de serviços. 
            O ano de <b>{ano_sel}</b> apresenta um PIB nominal de {formatar_valor(dados_atuais['PIB'])}.</p>
            <p>Este Observatório utiliza Ciência de Dados para mapear o impacto da <b>Indústria 4.0</b> no VAB local.</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📜 Plano Diretor", "🗺️ Zoneamento"])
        with tab1:
            st.write("Análise sobre a Lei Complementar 002/10 e restrições de expansão industrial próxima a áreas residenciais.")
        with tab2:
            st.link_button("Abrir Mapa Georreferenciado", "https://www.votorantim.sp.gov.br/arquivos/mapas_002_19043716.pdf")
            
    with c2:
        st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=150)
        st.info("💡 Dica: Utilize o controle lateral para navegar entre os anos da série histórica.")

elif menu == "Análise de Problemas":
    st.markdown('<h1 class="section-header">Matriz de Riscos e Desafios</h1>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="card-bi" style="border-left: 6px solid #ef4444;">
            <h4 style="color:#ef4444;">Efeito Shadowing</h4>
            <p>Perda de competitividade e fuga de investimentos para o polo industrial de Sorocaba.</p>
        </div>
        <div class="card-bi" style="border-left: 6px solid #f59e0b;">
            <h4 style="color:#f59e0b;">Conflitos Urbanos</h4>
            <p>Áreas industriais cercadas por avanços imobiliários, gerando restrições de ruído e logística.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="card-bi" style="border-left: 6px solid #3b82f6;">
            <h4 style="color:#3b82f6;">Desindustrialização Precoce</h4>
            <p>Risco de transição para serviços de baixo valor agregado sem modernização das plantas fabris.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Pipeline de Dados":
    st.markdown('<h1 class="section-header">Arquitetura de Dados (ETL)</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="etl-step">
        <b>1. Extração (Extraction):</b> Consumo de APIs do IBGE (SIDRA), SEADE e bases do Novo CAGED.
    </div>
    <div class="etl-step">
        <b>2. Transformação (Transformation):</b> Padronização de escalas financeiras, deflação via IPCA histórico e limpeza de CNAEs.
    </div>
    <div class="etl-step">
        <b>3. Carga (Loading):</b> Estruturação em Dataframes Pandas para renderização em tempo real no Streamlit.
    </div>
    """, unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    st.markdown(f'<h1 class="section-header">Panorama Econômico - {ano_sel}</h1>', unsafe_allow_html=True)
    
    # KPIs principais
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="metric-container">PIB TOTAL<br><h2>{formatar_valor(dados_atuais["PIB"])}</h2></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-container">VAB INDÚSTRIA<br><h2>{formatar_valor(dados_atuais["VAB_Industria"])}</h2></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-container">VAB SERVIÇOS<br><h2>{formatar_valor(dados_atuais["VAB_Servicos"])}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos
    col_g1, col_g2 = st.columns([3, 2])
    with col_g1:
        fig_evol = px.area(df_hist, x="Ano", y=["VAB_Industria", "VAB_Servicos"], 
                           title="Evolução do Valor Adicionado Bruto",
                           color_discrete_sequence=["#1e3a8a", "#3b82f6"])
        st.plotly_chart(fig_evol, use_container_width=True)
    with col_g2:
        fig_pie = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4,
                         title="Share por Segmento", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

elif menu == "Diagnóstico 4.0":
    st.markdown('<h1 class="section-header">Indicadores de Maturidade Digital</h1>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="card-bi">', unsafe_allow_html=True)
        st.write("**Maturidade por Setor (Radar)**")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="card-bi">', unsafe_allow_html=True)
        st.write("**Ganho Potencial de Eficiência**")
        st.progress(35, text="Produtividade Operacional (+35%)")
        st.progress(20, text="Redução de Desperdícios (+20%)")
        st.progress(15, text="Redução em Custos de Manutenção (+15%)")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Plano de Ação":
    st.markdown('<h1 class="section-header">Diretrizes Estratégicas</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="card-bi">
            <h4 style="color:#3b82f6;">1. Hub de Inovação Votorantim</h4>
            <p>Criação de centros de treinamento técnico em parceria com FATEC e SENAI focados em IoT e Manutenção Preditiva.</p>
        </div>
        <div class="card-bi">
            <h4 style="color:#3b82f6;">2. Incentivos Fiscais 4.0</h4>
            <p>Isenção parcial de ISS para indústrias que implementarem sistemas de digitalização e servitização.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.link_button("📂 Acessar Repositório Completo (Google Drive)", 
                   "https://drive.google.com/drive/folders/12XwL_9c_lzHLopxX9lHEeNBGkn1old8G")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 2rem;">
        Observatório Industrial Votorantim | Desenvolvido para Inteligência 4.0<br>
        Grupo: Bruno V. Queiroz, Gislaine Takushi, Mariana Curvêlo, Victor Perillo e Vinicius Pierote.
    </div>
""", unsafe_allow_html=True)
