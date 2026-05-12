import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import segno
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial Votorantim | Inteligência 4.0",
    page_icon="🏭",
    layout="wide"
)

# --- SISTEMA DE DESIGN (CSS AVANÇADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* Cards Estilizados */
    .card-bi {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .section-header {
        color: #1e3a8a;
        font-size: 1.8rem;
        font-weight: 700;
        border-left: 8px solid #ff8c00;
        padding-left: 15px;
        margin-bottom: 25px;
    }

    /* Estilização de Métricas */
    [data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }

    /* ETL Box Modernizado */
    .step-box { 
        padding: 1.2rem; border-radius: 10px; margin-bottom: 1rem; border-left: 6px solid; 
    }
    .step-extracao { background-color: #eff6ff; border-color: #1e3a8a; color: #1e3a8a; }
    .step-transformacao { background-color: #fffaf5; border-color: #ff8c00; color: #854d0e; }
    .step-carga { background-color: #f0fdf4; border-color: #22c55e; color: #166534; }

    /* Zoneamento Cards */
    .z-card { 
        background-color: #f1f5f9; padding: 1rem; border-radius: 8px; 
        border-left: 4px solid #ff8c00; margin-bottom: 10px; min-height: 80px;
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] { background-color: #0f172a; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    .footer {
        text-align: center; padding: 3rem; color: #64748b; font-size: 0.85rem;
        border-top: 1px solid #e2e8f0; margin-top: 4rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES E SUPORTE ---
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
        'Ano': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'PIB': [670.405, 791.318, 844.845, 914.154, 1124.655, 1357.128, 1561.842, 1811.097, 2042.691, 2094.207, 2482.293, 2975.838, 4672.147, 4495.059, 3076.565, 2995.815, 3093.050, 3405.739, 3412.630, 3919.236, 4518.922, 5209.654],
        'PIB_Constante': [2738.300, 2872.278, 2805.643, 2821.385, 3284.191, 3842.402, 4233.203, 4635.299, 5012.020, 4851.686, 5399.786, 6116.218, 9066.783, 8197.656, 5069.796, 4644.585, 4657.926, 4943.435, 4748.766, 5217.874, 5466.351, 5956.990],
        'VAB_Industria': [234.6, 276.9, 295.7, 319.9, 393.6, 475.0, 546.6, 633.9, 714.9, 732.9, 868.8, 1041.5, 1635.2, 1573.3, 1076.8, 1048.5, 1082.6, 1192.0, 1194.4, 1371.7, 1581.6, 1823.4],
        'VAB_Servicos': [368.7, 435.2, 464.7, 502.8, 618.6, 746.4, 859.0, 996.1, 1123.5, 1151.8, 1365.3, 1636.7, 2569.7, 2472.3, 1692.1, 1647.7, 1701.2, 1873.1, 1876.9, 2155.6, 2485.4, 2865.3]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()
ipca_map = {
    2002: 12.53, 2003: 9.30, 2004: 7.60, 2005: 5.69, 2006: 3.14, 2007: 4.46, 2008: 5.90, 2009: 4.31, 2010: 5.91, 
    2011: 6.50, 2012: 5.84, 2013: 5.91, 2014: 6.41, 2015: 10.67, 2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31, 
    2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.83, 2025: 4.26
}

# --- SIDEBAR ---
with st.sidebar:
    col_logo, col_qr = st.columns([1, 1])
    with col_logo:
        st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=70)
    with col_qr:
        url_da_pagina = "https://economiaapp-economia-fatec.streamlit.app/" 
        st.image(gerar_qrcode(url_da_pagina), width=75)
        st.caption("Acesse aqui")

    st.title("Inteligência Industrial")
    st.subheader("Votorantim 4.0")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                    ["Introdução & Contexto", "Problemas Identificados", "Metodologia ETL", 
                    "Dashboard Executivo", "Diagnóstico Indústria 4.0", "Projeção Futura", 
                    "Plano de Ação", "Fontes/Referências"])

# --- LÓGICA DE FILTRO ---
if ano_selecionado == "Todos":
    dados_atuais = df_hist.iloc[-1]
    ano_txt = "Último Dado (2023)"
else:
    dados_atuais = df_hist[df_hist['Ano'] == int(ano_selecionado)].iloc[0]
    ano_txt = ano_selecionado

# --- MÓDULOS ---

if menu == "Introdução & Contexto":
    st.markdown('<p class="section-header">Contexto e Plano Diretor</p>', unsafe_allow_html=True)
    tab_econ, tab_diretor, tab_urbano = st.tabs(["📊 Análise Econômica", "📜 Plano Diretor", "🗺️ Zoneamento"])
    
    with tab_econ:
        st.markdown(f"""<div class="card-bi">
            <h3>Observatório Econômico Votorantim: Da Base Industrial à Inteligência de Dados</h3>
            Votorantim atravessa um momento crucial de transição econômica. Historicamente consolidada como um pilar da indústria de base (minerais e metalurgia), a cidade hoje apresenta uma nova dinâmica revelada pelos dados: a ascensão acelerada do setor de serviços e um aumento expressivo na produtividade por operário.<br><br>
            Este dashboard utiliza técnicas avançadas de Ciência de Dados para monitorar essa evolução, integrando fontes oficiais (IBGE, SEADE, CAGED) em um pipeline ETL automatizado. Nosso objetivo é fornecer uma visão estratégica sobre o fenômeno de <b>"Shadowing"</b> em relação a Sorocaba e identificar como a Indústria 4.0 pode atuar como o motor para a retenção de talentos e o crescimento do VAB municipal no próximo decênio.
        </div>""", unsafe_allow_html=True)

    with tab_diretor:
        st.markdown("""<div class="card-bi">
            Votorantim possui um <b>Plano Diretor</b> que organiza o crescimento da cidade e define onde atividades industriais podem se instalar. Em teoria, o município permite a instalação de indústrias, desde que elas estejam localizadas nas zonas adequadas e atendam aos critérios legais.<br><br>
            Na prática, porém, o cenário atual cria dificuldades. As áreas industriais são limitadas e o crescimento urbano gerou conflitos por ruído e logística. O avanço urbano e restrições ambientais (como a Represa de Itupararanga) tornam o processo cada vez mais difícil para empresas de grande porte.<br><br>
            <small>Fonte: <a href="https://www.votorantim.sp.gov.br/plano-diretor-lei-vigente-anexos" target="_blank">votorantim.sp.gov.br/plano-diretor</a></small>
        </div>""", unsafe_allow_html=True)

    with tab_urbano:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="z-card"><b>Conflito Urbano-Industrial:</b> O avanço de bairros residenciais gera restrições de ruído.</div>', unsafe_allow_html=True)
            st.markdown('<div class="z-card"><b>Topografia Desfavorável:</b> Relevo acidentado eleva custos de terraplenagem.</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="z-card"><b>Competição com Sorocaba:</b> Fuga de investimentos para distritos industriais vizinhos.</div>', unsafe_allow_html=True)
            st.markdown('<div class="z-card"><b>Restrições Ambientais:</b> Proximidade com mananciais limita atividades.</div>', unsafe_allow_html=True)
        st.link_button("🔍 Abrir Mapa de Zoneamento Oficial", "https://www.votorantim.sp.gov.br/arquivos/mapas_002_19043716.pdf", use_container_width=True)

elif menu == "Problemas Identificados":
    st.markdown('<p class="section-header">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Clusterização e Dependência**: O ecossistema é dependente de poucos players gigantes. Isso gera risco sistêmico.")
        st.warning("**Conflito Territorial:** Trade-off entre expansão imobiliária e manutenção da produção fabril.")
    with c2:
        st.success("**Evolução Setorial:** O risco é a desindustrialização precoce se o setor de serviços for de baixo valor agregado.")
        st.info("**Efeito Shadowing:** Perda de talentos e investimentos diretos para Sorocaba.")

elif menu == "Metodologia ETL":
    st.markdown('<p class="section-header">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    st.markdown('''
        <div class="step-box step-extracao"><b>1. Extração:</b> Coleta de dados brutos do IBGE, SEADE e Novo CAGED.</div>
        <div class="step-box step-transformacao"><b>2. Transformação:</b> Limpeza de nulos, padronização CNAE e unificação de bases via Ano.</div>
        <div class="step-box step-carga"><b>3. Carregamento:</b> Estruturação em DataFrames para consumo no Streamlit.</div>
    ''', unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    st.markdown(f'<p class="section-header">Panorama Macro de Votorantim - {ano_txt}</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric(f"PIB Municipal", formatar_valor(dados_atuais['PIB']))
    c2.metric("VAB Indústria (Est.)", formatar_valor(dados_atuais['VAB_Industria']))
    c3.metric("VAB Serviços (Est.)", formatar_valor(dados_atuais['VAB_Servicos']))

    # Gráfico PIB (Preços Correntes vs Constantes)
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB'], name='PIB Corrente', marker_color='#1E3A8A'))
    fig_comp.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB_Constante'], name='PIB Constante (2023)', marker_color='#E67E22'))
    fig_comp.update_layout(title="Evolução do PIB (R$ Mil)", barmode='group', legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_comp, use_container_width=True)

    if st.button("Inserir Impacto IPCA"):
        st.session_state.dash_ipca = not st.session_state.get('dash_ipca', False)

    if st.session_state.get('dash_ipca', False):
        df_p = df_hist.copy()
        ipca_f = {k: v for k, v in ipca_map.items() if k <= 2023}
        df_p['Fator'] = [(np.prod([(1 + ipca_f[y]/100) for y in ipca_f if y <= ano])) for ano in df_p['Ano']]
        df_p['Indústria (Real)'] = df_p['VAB_Industria'] / df_p['Fator']
        df_p['Serviços (Real)'] = df_p['VAB_Servicos'] / df_p['Fator']
        st.plotly_chart(px.line(df_p, x='Ano', y=['VAB_Industria', 'Indústria (Real)', 'VAB_Servicos', 'Serviços (Real)'], title="Impacto Real vs Nominal"), use_container_width=True)
    
    st.plotly_chart(px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE"), use_container_width=True)

elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-header">Geração Digital e Impactos 4.0</p>', unsafe_allow_html=True)
    st.warning("**Nota:** Projeções baseadas em médias nacionais de ganhos de eficiência.")
    
    st.markdown("""<div class="card-bi">
        <h3 style="color:#1e3a8a">A Revolução 4.0 em Votorantim</h3>
        A Indústria 4.0 integra IoT, Big Data e IA. Fábricas Inteligentes reduzem desperdícios e aumentam competitividade.
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_prod = go.Figure(go.Bar(x=['Sem 4.0', 'Com 4.0'], y=[210, 345], marker_color=['#94a3b8', '#ff8c00'], text=['R$ 210k', 'R$ 345k'], textposition='auto'))
        fig_prod.update_layout(title="Diferença de Produtividade: +35%")
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_r = go.Figure(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker_color='#ff8c00'))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_r, use_container_width=True)

elif menu == "Projeção Futura":
    st.markdown('<p class="section-header">Análise Preditiva até 2030</p>', unsafe_allow_html=True)
    
    # Lógica Regressão Linear original
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2024, 2031)
    
    def projetar(x_h, y_h, x_p):
        coef = np.polyfit(x_h, y_h, 1)
        p = np.poly1d(coef)
        r2 = 1 - (np.sum((y_h - p(x_h))**2) / np.sum((y_h - np.mean(y_h))**2))
        return p(x_p), r2

    proj_ind, r2_i = projetar(anos_hist, df_hist['VAB_Industria'].values, anos_proj)
    proj_ser, r2_s = projetar(anos_hist, df_hist['VAB_Servicos'].values, anos_proj)

    df_proj = pd.concat([
        df_hist[['Ano', 'VAB_Industria', 'VAB_Servicos']].assign(Tipo='Histórico'),
        pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': proj_ind, 'VAB_Servicos': proj_ser, 'Tipo': 'Projeção'})
    ])
    
    st.plotly_chart(px.line(df_proj, x='Ano', y=['VAB_Industria', 'VAB_Servicos'], line_dash='Tipo', title="Projeção Econômica 2030"), use_container_width=True)
    st.info(f"Estatísticas de Confiança (R²): Indústria {r2_i:.2f} | Serviços {r2_s:.2f}")

elif menu == "Plano de Ação":
    st.markdown('<p class="section-header">Plano Estratégico 4.0</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card-bi"><h4>1. Modernização</h4>Isenção de ISS/IPTU para empresas que investirem em IoT.</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-bi"><h4>2. Zoneamento</h4>Criar zonas de amortecimento entre residências e fábricas limpas.</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="card-bi"><h4>3. Talentos</h4>Hub de Inovação Industrial com FATEC para combater o Shadowing.</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-bi"><h4>4. Servitização</h4>Apoiar startups de logística e manutenção preditiva local.</div>', unsafe_allow_html=True)

elif menu == "Fontes/Referências":
    st.markdown('<p class="section-header">Fontes e Bibliografia</p>', unsafe_allow_html=True)
    st.write("- **IBGE Cidades** | **Fundação SEADE** | **Novo CAGED**")
    st.write("- **Plano Diretor Votorantim** | **BCB/IBGE (IPCA)**")
    url_drive = "https://drive.google.com/drive/folders/12XwL_9c_lzHLopxX9lHEeNBGkn1old8G?usp=drive_link"
    st.image(gerar_qrcode(url_drive), width=150)
    st.link_button("📂 Abrir Pasta de Dados (Drive)", url_drive)

# --- FOOTER ---
st.markdown("""<div class="footer">
    <b>Observatório Industrial Votorantim | Inteligência Industrial 4.0</b><br>
    Grupo: Bruno V. Queiroz, Gislaine Takushi, Mariana Curvêlo, Victor Perillo e Vinicius Pierote.
</div>""", unsafe_allow_html=True)
