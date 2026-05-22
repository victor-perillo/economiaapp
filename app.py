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

# --- CUSTOMIZAÇÃO CSS (FRONT-END MODERNO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-size: 18px; color: #0f172a; }
    body, p, li, span, div, a, button, input, label, select { font-size: 1.05rem; line-height: 1.75; }
    .stApp { background-color: #f8fafc; }
    
    .card {
        background: white;
        padding: 2.4rem;
        border-radius: 20px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        border: none;
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #0f172a;
        font-size: 2.9rem;
        font-weight: 800;
        border-left: 10px solid #ff8c00;
        padding-left: 22px;
        margin-top: 20px;
        margin-bottom: 36px;
    }
    .stApp h3, .stApp h4 { color: #0f172a; }
    .stApp h3 { font-size: 2.2rem; margin-bottom: 1rem; }
    .stApp h4 { font-size: 1.55rem; margin-bottom: 0.75rem; }

    .step-box { 
        padding: 1.8rem; border-radius: 12px; margin-bottom: 1.2rem; border-left: 8px solid; 
        font-size: 1.05rem;
    }
    .step-extracao { background-color: #eff6ff; border-color: #1e3a8a; color: #1e3a8a; }
    .step-transformacao { background-color: #fffaf5; border-color: #ff8c00; color: #854d0e; }
    .step-carga { background-color: #f0fdf4; border-color: #22c55e; color: #166534; }

    .z-card { 
        background-color: #f1f5f9; padding: 1.6rem; border-radius: 16px; 
        border-left: 5px solid #ff8c00; margin-bottom: 18px; min-height: 130px;
        font-size: 1.05rem;
    }

    [data-testid="stSidebar"] { background-color: #0f172a; }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-size: 1.05rem !important; }
    [data-testid="stSidebar"] img { max-width: 120px !important; }
    [data-testid="stSidebar"] select, [data-testid="stSidebar"] .stSelectbox>div>div, [data-testid="stSidebar"] .stSelectbox>div>div>div,
    [data-testid="stSidebar"] .stTextInput>div>div>input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] .stSelectbox>label>div, [data-testid="stSidebar"] .stSelectbox>label>div span {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stSelectbox>div>div>div span { color: #ffffff !important; }
    .stButton>button { font-size: 1.1rem !important; padding: 0.9rem 1rem !important; }
    .stSelectbox, .stRadio { font-size: 1.1rem !important; }
    .css-1oe9bi0, .css-1d391kg, .css-hxt7ib { font-size: 1.1rem !important; }
    .stTextInput>div>div>input { font-size: 1.05rem !important; padding: 0.9rem !important; }
    
    .chart-caption { text-align: center; color: #475569; font-style: italic; margin-top: 14px; font-size: 1.05rem; }
    .footer {
        text-align: center; padding: 3.2rem; color: #475569; font-size: 1.05rem;
        border-top: 1px solid #e2e8f0; margin-top: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES E SUPORTE ---
def formatar_valor(valor):
    if valor >= 1000:
        return f"R$ {valor/1000:.2f} Bi"
    return f"R$ {valor:.1f} Mi"

def gerar_qrcode(url):
    qrcode = segno.make_qr(url)
    out = BytesIO()
    qrcode.save(out, kind='png', scale=10)
    return out.getvalue()

# --- CARREGANDO OS DADOS ---
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

def style_figure(fig, title_size=20, legend=True):
    layout_options = dict(
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=16, color='#0f172a'),
        title_font=dict(family='Inter, sans-serif', size=title_size, color='#0f172a'),
        plot_bgcolor='#f8fafc',
        paper_bgcolor='white',
        margin=dict(t=90, b=60, l=60, r=40),
    )
    if legend:
        layout_options['legend'] = dict(font=dict(size=14), orientation='h', y=-0.2, x=0.5, xanchor='center')
    else:
        layout_options['showlegend'] = False
    fig.update_layout(**layout_options)
    try:
        fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(size=14))
    except Exception:
        pass
    try:
        fig.update_yaxes(showgrid=True, gridcolor='rgba(15, 23, 42, 0.08)', zeroline=False, tickfont=dict(size=14))
    except Exception:
        pass
    return fig

ipca_map = {
    2002: 12.53, 2003: 9.30, 2004: 7.60, 2005: 5.69, 2006: 3.14, 2007: 4.46, 2008: 5.90, 2009: 4.31, 2010: 5.91, 
    2011: 6.50, 2012: 5.84, 2013: 5.91, 2014: 6.41, 2015: 10.67, 2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31, 
    2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.83, 2025: 4.26
}

employment_total = 26700

gender_df = pd.DataFrame({
    'Gênero': ['Homens', 'Mulheres'],
    'Vínculos': [13400, 13300],
    'Percentual': [50.2, 49.8]
})

sector_df = pd.DataFrame({
    'Setor Econômico': ['Serviços', 'Comércio', 'Indústria', 'Construção'],
    'Percentual': [47.0, 26.0, 22.1, 4.9],
    'Vínculos': [12549, 6608, 5900, 1300]
})

age_df = pd.DataFrame({
    'Faixa Etária': ['30 a 49 anos', '50 a 64 anos', '14 a 24 anos', '25 a 29 anos', '65 anos ou mais'],
    'Percentual': [50.3, 18.8, 16.2, 13.4, 1.4]
})

gdp_sector_df = pd.DataFrame({
    'Setor Econômico': ['Serviços', 'Indústria', 'Administração Pública', 'Agropecuária'],
    'Participação PIB': [61.5, 17.5, 18.0, 0.5]
})

employment_trend = pd.DataFrame({
    'Ano': [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Vínculos': [24300, 24350, 24370, 24380, 24390, 24390, 24390, 24850, 25500, 26700]
})

# --- SIDEBAR ---
with st.sidebar:
    col_logo, col_qr = st.columns([1, 1])
    with col_logo:
        st.image("https://img.icons8.com/ios-filled/96/ffffff/factory.png", width=90)
    with col_qr:
        url_da_pagina = "https://economiaapp-economia-fatec.streamlit.app/" 
        st.image(gerar_qrcode(url_da_pagina), width=110)
        st.caption("Acesse aqui")

    st.title("Inteligência Industrial")
    st.subheader("Votorantim 4.0")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis)
    st.markdown(f"**Período selecionado:** {ano_selecionado}")
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                    ["Introdução & Contexto", "Problemas Identificados", "Metodologia ETL", 
                    "Dashboard Executivo", "Diagnóstico Indústria 4.0", "Projeção Futura", 
                    "Plano de Ação", "Fontes/Referências"])

# --- LÓGICA DE FILTROS ---
if ano_selecionado == "Todos":
    dados_atuais = pd.Series({
        'PIB': df_hist['PIB'].iloc[-1],
        'VAB_Industria': df_hist['VAB_Industria'].iloc[-1],
        'VAB_Servicos': df_hist['VAB_Servicos'].iloc[-1]
    })
    ano_txt = "Último Dado (2023)"
else:
    display_df = df_hist[df_hist['Ano'] == int(ano_selecionado)]
    dados_atuais = display_df.iloc[0]
    ano_txt = ano_selecionado

# --- MÓDULOS ---

if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Contexto e Plano Diretor</p>', unsafe_allow_html=True)
    tab_econ, tab_diretor, tab_urbano = st.tabs(["📊 Análise Econômica", "📜 Plano Diretor de Votorantim", "🗺️ Zoneamento Urbano"])
    
    with tab_econ:
        st.markdown("""
        <div class="card">
            <h3>Observatório Econômico Votorantim: Da Base Industrial à Inteligência de Dados</h3>
            Votorantim atravessa um momento crucial de transição econômica. Historicamente consolidada como um pilar da indústria de base (minerais e metalurgia), a cidade hoje apresenta uma nova dinâmica revelada pelos dados: a ascensão acelerada do setor de serviços e um aumento expressivo na produtividade por operário.
            <br><br>
            Este dashboard utiliza técnicas avançadas de Ciência de Dados para monitorar essa evolução, integrando fontes oficiais (IBGE, SEADE, CAGED) em um pipeline ETL automatizado. Nosso objetivo é fornecer uma visão estratégica sobre o fenômeno de <b>"Shadowing"</b> em relação a Sorocaba e identificar como a Indústria 4.0 pode atuar como o motor para a retenção de talentos e o crescimento do VAB municipal no próximo decênio.
        </div>
        """, unsafe_allow_html=True)

    with tab_diretor:
        st.markdown("""
        <div class="card">
            Votorantim possui um <b>Plano Diretor</b> que organiza o crescimento da cidade e define onde atividades industriais podem se instalar, sempre respeitando regras de uso do solo e exigências ambientais. Em teoria, o município permite a instalação de indústrias, desde que elas estejam localizadas nas zonas adequadas e atendam aos critérios legais.
            <br><br>
            Na prática, porém, o cenário atual cria dificuldades. As áreas industriais são limitadas e, com o crescimento da cidade, many delas passaram a ficar próximas ou até “encostadas” em regiões urbanas. Isso gera conflitos, pois aumenta a exigência por controle de impactos como ruído, trânsito de caminhões e poluição, restringindo principalmente a instalação de indústrias de maior porte.
            <br><br>
            Além disso, existem restrições ambientais importantes que reduzem ainda mais o espaço disponível, somadas a processos burocráticos e custos de adequação. O resultado é que, embora não haja proibição, há uma limitação prática: poucas áreas realmente viáveis e um nível alto de exigência para novos empreendimentos.
            <br><br>
            Em resumo, Votorantim permite a instalação de indústrias, mas o avanço urbano, as restrições ambientais e a escassez de zonas industriais adequadas tornam esse processo cada vez mais difícil, especialmente para empresas maiores ou com maior impacto.
            <br><br>
            <small>Fonte: <a href="https://www.votorantim.sp.gov.br/plano-diretor-lei-vigente-anexos" target="_blank">votorantim.sp.gov.br/plano-diretor</a></small>
        </div>
        """, unsafe_allow_html=True)

    with tab_urbano:
        st.markdown('### Desafios do Ordenamento Territorial')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="z-card"><b>Conflito Urbano-Industrial:</b> O avanço de bairros residenciais sobre áreas fabris gera restrições de ruído e logística, criando insegurança jurídica para grandes plantas industriais.</div>', unsafe_allow_html=True)
            st.markdown('<div class="z-card"><b>Topografia Desfavorável:</b> O relevo acidentado de muitas zonas industriais eleva os custos de terraplenagem e encarece a construção de galpões e acessos.</div>', unsafe_allow_html=True)
            st.markdown('<div class="z-card"><b>Restrições Ambientais:</b> A proximidade com mananciais e áreas de preservação (como a região da Represa de Itupararanga) exige licenciamentos rigorosos e limita o tipo de atividade permitida.</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="z-card"><b>Competição com Sorocaba:</b> A cidade vizinha oferece distritos industriais mais consolidados e planos diretores que facilitam a instalação rápida, gerando uma fuga de investimentos para o município vizinho.</div>', unsafe_allow_html=True)
            st.markdown('<div class="z-card"><b>Infraestrutura de Acesso:</b> Dificuldade em escoar carga pesada sem atravessar perímetros urbanos adensados, o que sobrecarrega o trânsito local e atrasa a logística.</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.image("Zoneamento Urbano Vot.png", caption="Mapa de Zoneamento Urbano de Votorantim", width=1000)
        pdf_url = "https://www.votorantim.sp.gov.br/arquivos/mapas_002_19043716.pdf"
        st.link_button("🔍 Abrir Mapa de Zoneamento", pdf_url, use_container_width=True)

elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("""**Clusterização e Dependência em relação ao PIB**: O ecossistema é muito dependente de poucos players gigantes (como: Grupo Votorantim, Splice, Gás Natural e FLSmidth). 
        Em termos de risco de negócio, isso é perigoso: se uma dessas verticais sofre um choque, o impacto no município é sistêmico.""")
        st.warning("""**Conflito Territorial:** O avanço do setor imobiliário sobre áreas industriais cria barreiras para a escalabilidade das fábricas. 
        É um problema de Trade-off entre expansão urbana e manutenção da produção.""")
    with c2:
        st.success("""**Evolução Setorial:** Apesar de ser um sinal de modernização, o risco é a desindustrialização precoce. Se a indústria enfraquecer rápido demais e o setor de serviços for apenas de 'baixo valor agregado' (como pequenos comércios ou serviços básicos), a renda média da cidade cai.""")
        st.info("""**Efeito Shadowing:** Ocorre quando Votorantim perde talentos e investimentos para Sorocaba. 
        Isso resulta em uma economia local estagnada, focada em setores de baixo valor agregado.""")

elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    st.markdown('''
        <div class="step-box step-extracao">
            <b>1. Extração:</b><br>
            Ação: Coletamos dados brutos de três fontes governamentais distintas: IBGE Cidades (Séries históricas de PIB), SEADE (VAB por setor municipal) e Novo CAGED (Movimentação formal de empregos).<br>
            Formatos: CSV e consultas em tabelas do SIDRA/IBGE.
        </div>
        <div class="step-box step-transformacao">
            <b>2. Transformação:</b><br>
            Limpeza de Nulos: Removemos registros incompletos.<br>
            Padronização: Unificamos nomenclaturas CNAE e escalas financeiras (Mi/Bi).<br>
            Unificação (Join): Merge das bases de Emprego e PIB utilizando o Ano como chave primária.
        </div>
        <div class="step-box step-carga">
            <b>3. Carregamento:</b><br>
            Ação: O dataset limpo foi estruturado em DataFrames e exportado para formatos prontos para consumo no Streamlit.
        </div>
    ''', unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown("""<div class="card" style="min-height: 250px;">
            <h4 style="color:#1E3A8A;">O que é o PIB?</h4>
            O <b>Produto Interno Bruto (PIB)</b> representa a soma de todos os bens e serviços finais produzidos em uma região durante um período. É o principal indicador para medir a riqueza e o vigor econômico de um município.
        </div>""", unsafe_allow_html=True)
    with col_info2:
        st.markdown("""<div class="card" style="min-height: 250px;">
            <h4 style="color:#1E3A8A;">O que é o VAB?</h4>
            O <b>Valor Adicionado Bruto (VAB)</b> é o valor que cada setor (Indústria, Serviços, Agro) adiciona à economia, deduzindo o custo dos insumos utilizados no processo produtivo. Reflete a contribuição real de cada atividade.
        </div>""", unsafe_allow_html=True)
    with col_info3:
        st.markdown("""<div class="card" style="min-height: 250px;">
            <h4 style="color:#1E3A8A;">Como são calculados?</h4>
            O <b>VAB</b> é calculado pela diferença entre o Valor Bruto da Produção e o Consumo Intermediário. O <b>PIB</b> é a soma dos VABs de todos os setores mais os impostos sobre produtos (líquidos de subsídios).
        </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']))
    with c2:
        st.metric("VAB Indústria (Est.)", formatar_valor(dados_atuais['VAB_Industria']))
    with c3:
        st.metric("VAB Serviços (Est.)", formatar_valor(dados_atuais['VAB_Servicos']))

    st.markdown("---")

    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB'], name='PIB Votorantim Corrente', marker_color='#1E3A8A'))
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB_Constante'], name='PIB Constante (2023)', marker_color='#E67E22'))
    fig_comparativo.update_layout(
        title="Evolução do PIB (Correntes vs Constantes de 2023), em R$ mil",
        xaxis_title="Ano", barmode='group', legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center")
    )

    if "aplicar_ipca_dash" not in st.session_state:
        st.session_state.aplicar_ipca_dash = False

    row_evolucao, row_historico = st.columns([0.55, 0.45])
    with row_evolucao:
        st.plotly_chart(fig_comparativo, use_container_width=True)
    with row_historico:
        if st.button("Inserir IPCA (Impacto Inflacionário Histórico até 2023)"):
            st.session_state.aplicar_ipca_dash = not st.session_state.aplicar_ipca_dash

        df_p = df_hist.copy()
        if st.session_state.aplicar_ipca_dash:
            ipca_filtered = {k: v for k, v in ipca_map.items() if k <= 2023}
            df_p['Fator'] = [(np.prod([(1 + ipca_filtered[y]/100) for y in ipca_filtered if y > ano])) for ano in df_p['Ano']]
            df_p['Indústria (Ajustado IPCA)'] = df_p['VAB_Industria'] * df_p['Fator']
            df_p['Serviços (Ajustado IPCA)'] = df_p['VAB_Servicos'] * df_p['Fator']
            y_cols = ['VAB_Industria', 'Indústria (Ajustado IPCA)', 'VAB_Servicos', 'Serviços (Ajustado IPCA)']
        else:
            y_cols = ['VAB_Industria', 'VAB_Servicos']

        fig_evolucao = px.line(df_p, x='Ano', y=y_cols, title="Evolução Histórica: Indústria vs Serviços", markers=True,
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "Indústria (Ajustado IPCA)": "#93c5fd", "VAB_Servicos": "#FF8C00", "Serviços (Ajustado IPCA)": "#fdba74"})
        fig_evolucao.update_layout(yaxis_title='Valor (R$ milhões)')
        style_figure(fig_evolucao, title_size=22)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">As séries históricas mostram valores menores inicialmente. Ao aplicar o IPCA, os valores ficam maiores e refletem a inflação histórica acumulada até 2023.</div>', unsafe_allow_html=True)

    st.markdown("---")

    dist_pib_col, obs_col = st.columns([0.6, 0.4])
    with dist_pib_col:
        fig_gdp_pie = px.pie(gdp_sector_df, names='Setor Econômico', values='Participação PIB',
                             title='Participação Estimada no PIB (2023)', hole=0.3,
                             color='Setor Econômico', color_discrete_sequence=['#1E40AF', '#0EA5E9', '#9333EA', '#22C55E'])
        fig_gdp_pie.update_traces(texttemplate='%{label}: %{percent:.1%}', textposition='outside', textfont_size=14, insidetextorientation='radial')
        style_figure(fig_gdp_pie, title_size=22, legend=True)
        fig_gdp_pie.update_layout(legend=dict(orientation='v', x=1.02, y=0.5, xanchor='left', yanchor='middle', font=dict(size=14)))
        st.plotly_chart(fig_gdp_pie, use_container_width=True)
    with obs_col:
        st.markdown("""<div class=\"card\" style=\"min-height: 180px;\">\n            <h4>Observação de Participação</h4>\n            <p style=\"margin:0;\">Serviços representam a maior fatia estimada do PIB, enquanto Agropecuária chega a menos de 1%.</p>\n            <p style=\"color:#64748b; margin-top:0.5rem;\">Indústria e Administração Pública ocupam cerca de 35% do PIB local.</p>\n        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    ref_col, cnae_col = st.columns(2)
    with ref_col:
        st.write("**Referência IPCA Aplicada (até 2023):**")
        ipca_exec_tab = pd.DataFrame([(k, v) for k, v in ipca_map.items() if k <= 2023], columns=['Ano', 'IPCA (%)'])
        st.dataframe(ipca_exec_tab, hide_index=True, height=250)
    with cnae_col:
        fig_cnae = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE")
        fig_cnae.update_traces(texttemplate='%{label}: %{percent:.1%}', textposition='outside', textfont_size=13, insidetextorientation='radial')
        style_figure(fig_cnae, title_size=20, legend=True)
        fig_cnae.update_layout(legend=dict(orientation='v', x=1.02, y=0.5, xanchor='left', yanchor='middle', font=dict(size=14)))
        st.plotly_chart(fig_cnae, use_container_width=True)

    st.markdown("---")
    st.markdown('<h3>Distribuição de Empregos em Votorantim</h3>', unsafe_allow_html=True)
    emp_card_col, emp_trend_col = st.columns([0.4, 0.6])
    with emp_card_col:
        st.markdown(f"""<div class=\"card\" style=\"min-height: 180px;\">\n            <h4>Total de Empregos Formais</h4>\n            <p style=\"font-size:2rem; margin:0;\"><b>{employment_total/1000:.1f} mil</b></p>\n            <p style=\"color:#64748b; margin-top:0.5rem;\">Vínculos formais registrados em Votorantim em 2023.</p>\n        </div>""", unsafe_allow_html=True)
    with emp_trend_col:
        fig_trend = px.line(employment_trend, x='Ano', y='Vínculos', title='Evolução dos Empregos Formais (2014-2023)', markers=True)
        fig_trend.update_layout(yaxis_title='Vínculos formais', xaxis=dict(dtick=1))
        style_figure(fig_trend, title_size=22)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    row_job1, row_job2 = st.columns(2)
    with row_job1:
        fig_sector_bar = px.bar(sector_df, x='Setor Econômico', y='Percentual', title='Distribuição por Setor (2023)',
                                text='Percentual', color='Setor Econômico', color_discrete_sequence=px.colors.qualitative.Safe)
        fig_sector_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=13)
        fig_sector_bar.update_layout(yaxis_title='Percentual (%)', showlegend=False)
        style_figure(fig_sector_bar, title_size=22, legend=False)
        st.plotly_chart(fig_sector_bar, use_container_width=True)
    with row_job2:
        fig_gender = px.pie(gender_df, names='Gênero', values='Vínculos', title='Divisão por Gênero (2023)',
                            color_discrete_map={'Homens': '#1E40AF', 'Mulheres': '#DB2777'}, hole=0.3)
        fig_gender.update_traces(texttemplate='%{label}: %{percent:.1%}', textposition='outside', textfont_size=14, insidetextorientation='radial')
        style_figure(fig_gender, title_size=22, legend=False)
        fig_gender.update_layout(
            legend=dict(orientation='h', y=-0.18, x=0.5, xanchor='center', font=dict(size=14)),
            margin=dict(t=90, b=120, l=40, r=40)
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")
    row_job3, row_job4 = st.columns(2)
    with row_job3:
        fig_treemap = px.treemap(sector_df, path=['Setor Econômico'], values='Vínculos',
                                 title='Distribuição por Setor de Atividade (2023)',
                                 color='Percentual', color_continuous_scale='Blues')
        fig_treemap.update_traces(textinfo='label+value+percent parent')
        style_figure(fig_treemap, title_size=22, legend=False)
        st.plotly_chart(fig_treemap, use_container_width=True)
    with row_job4:
        fig_age = px.pie(age_df, names='Faixa Etária', values='Percentual', title='Distribuição por Faixa Etária (2023)', hole=0.3)
        fig_age.update_traces(texttemplate='%{label}: %{percent:.1%}', textposition='outside', textfont_size=14, insidetextorientation='radial')
        style_figure(fig_age, title_size=22, legend=True)
        fig_age.update_layout(legend=dict(orientation='v', x=1.02, y=0.5, xanchor='left', yanchor='middle', font=dict(size=14)))
        st.plotly_chart(fig_age, use_container_width=True)

elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Votorantim 4.0: Projeções de Competitividade Industrial</p>', unsafe_allow_html=True)
    st.info("""
        Estas projeções consideram a adoção de tecnologias da Indústria 4.0 como fator diferenciador na competitividade local. 
        O cenário está baseado em benchmarks nacionais e avaliação setorial de maturidade digital.
    """)

    st.markdown("""
    <div class="card">
        <h3 style="color: #1E3A8A;">Evolução Industrial: Projeção de Ganhos com a Tecnologia 4.0</h3>
        <p>A <b>Indústria 4.0</b> combina IoT, Big Data, IA e automação para transformar a produção de fábricas tradicionais em operações mais eficientes, resilientes e escaláveis.</p>
        <div style="display:flex; flex-wrap:wrap; gap:15px; margin-top:20px;">
            <div class="z-card" style="flex:1; min-width:220px;"><b>Ganho de Eficiência:</b> Menos retrabalho e menos desperdício por meio de monitoramento contínuo.</div>
            <div class="z-card" style="flex:1; min-width:220px;"><b>Manutenção Preditiva:</b> Identificação precoce de falhas para reduzir paradas não programadas.</div>
            <div class="z-card" style="flex:1; min-width:220px;"><b>Customização Ágil:</b> Atender pedidos com maior rapidez e menores custos de setup.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([0.6, 0.4])
    with c1:
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=['Sem Tecnologia 4.0', 'Com Tecnologia 4.0'], y=[210, 345], marker_color=['#94a3b8', '#FF8C00'], text=['R$ 210k', 'R$ 345k'], textposition='auto', marker_line_color='rgba(0,0,0,0.08)', marker_line_width=1.5))
        fig_comp.add_hline(y=280, line_dash="dash", line_color="#0B5394", line_width=4,
                           annotation_text="Média Nacional: R$ 280k", annotation_position="top left",
                           annotation_font_size=12, annotation_font_color="#0B5394")
        fig_comp.update_layout(
            title="Produtividade por Operário: Tecnologia 4.0 vs Modelo Tradicional",
            yaxis_title="R$ / Operário (Milhares)",
            xaxis_title="",
            bargap=0.35,
            margin=dict(t=80, b=40)
        )
        style_figure(fig_comp, title_size=22, legend=False)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('<div class="chart-caption">Linha pontilhada em destaque representa a produtividade média nacional. A adoção de 4.0 mostra ganho claro em relação a esse patamar.</div>', unsafe_allow_html=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=12))),
            title="Maturidade 4.0 por Segmento",
            margin=dict(t=70, b=40)
        )
        style_figure(fig_radar, title_size=22, legend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('<div class="chart-caption">Segmentos com maior maturidade digital indicam onde a transição 4.0 pode gerar impacto mais rápido.</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_text, col_metrics = st.columns([0.6, 0.4])
    with col_text:
        st.markdown("""
        <div class="card"><h4 style="color: #1E3A8A;">Oportunidade Estratégica</h4><ul style="margin:0; padding-left:18px; line-height:1.7;">
            <li>Votorantim pode posicionar suas plantas industriais acima da média nacional de produtividade.</li>
            <li>Investimentos em digitalização devem priorizar setores com maior maturidade e maior potencial de VAB.</li>
            <li>A integração de análise de dados e manutenção preditiva reduz custos operacionais e aumenta confiabilidade.</li>
        </ul></div>
        """, unsafe_allow_html=True)
    with col_metrics:
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Ganho Estimado", "+35%", "vs média nacional")
        with m2:
            st.metric("Impacto de Receita", "+R$ 65k", "por operário")
        st.markdown("""
        <div class="card" style="padding:1rem; margin-top:1rem;">
            <h4 style="color: #1E3A8A; margin-bottom:0.5rem;">Próximos passos</h4>
            <p style="margin:0;">1. Priorizar projetos de digitalização em metalurgia e química.<br>2. Definir indicadores claros de eficiência e redução de paradas.<br>3. Criar um roadmap 4.0 com metas de produtividade e ROI.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva e IPCA Previsionado (2030)</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3 style="color: #1E3A8A;">Análise de Tendência: O Caminho até 2030</h3>
        <p>Este gráfico utiliza <b>Regressão Linear</b> baseada na série de 21 anos para prever o futuro econômico municipal.</p>
        <div style="display: flex; gap: 15px;">
            <div class="z-card" style="flex:1;"><b>Crescimento Nominal:</b> Expansão sustentada baseada no histórico desde 2002.</div>
            <div class="z-card" style="flex:1;"><b>Crescimento Real:</b> Impacto da inflação futura e necessidade de inovação tecnológica.</div>
            <div class="z-card" style="flex:1;"><b>Confiabilidade (R²):</b> Robustez estatística das projeções para o decênio de 2030.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ano_final = 2030
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2024, ano_final + 1)

    def projetar(x_h, y_h, x_p):
        coef = np.polyfit(x_h, y_h, 1)
        p = np.poly1d(coef)
        r2 = 1 - (np.sum((y_h - p(x_h))**2) / np.sum((y_h - np.mean(y_h))**2))
        return p(x_p), r2

    p_ind, r2_ind = projetar(anos_hist, df_hist['VAB_Industria'].values, anos_proj)
    p_serv, r2_serv = projetar(anos_hist, df_hist['VAB_Servicos'].values, anos_proj)
    p_ipca, _ = projetar(np.array(list(ipca_map.keys())), np.array(list(ipca_map.values())), anos_proj)

    if st.button("Aplicar IPCA Previsionado"):
        st.session_state.mostrar_ipca_proj = not st.session_state.get('mostrar_ipca_proj', False)

    df_p_total = pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': p_ind, 'VAB_Servicos': p_serv, 'Tipo': 'Projeção'})
    if st.session_state.get('mostrar_ipca_proj', False):
        st.info("Ao aplicar o IPCA previsto, os valores projetados aumentam para a base inflacionada.")
        fatores = [np.prod([1 + v/100 for v in p_ipca[:i+1]]) for i in range(len(p_ipca))]
        df_p_total['Indústria (Ajustado IPCA)'] = df_p_total['VAB_Industria'] * fatores
        df_p_total['Serviços (Ajustado IPCA)'] = df_p_total['VAB_Servicos'] * fatores
        y_cols_p = ['VAB_Industria', 'Indústria (Ajustado IPCA)', 'VAB_Servicos', 'Serviços (Ajustado IPCA)']
    else:
        y_cols_p = ['VAB_Industria', 'VAB_Servicos']

    df_f = pd.concat([df_hist.assign(Tipo='Histórico'), df_p_total])
    fig_proj = px.line(df_f, x='Ano', y=y_cols_p, line_dash='Tipo', title="Projeção Econômica até 2030", 
                        color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"})
    style_figure(fig_proj, title_size=22)
    st.plotly_chart(fig_proj, use_container_width=True)
    st.info(f"**Estatísticas:** Indústria $R^2$: {r2_ind:.4f} | Serviços $R^2$: {r2_serv:.4f} | IPCA Médio Previsto: {np.mean(p_ipca):.2f}%")

elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">1: Modernização Industrial</h4><p><b>Ação:</b> Programa Votorantim 4.0.<br><b>Como:</b> Isenção parcial de ISS/IPTU para empresas que investirem em IoT e Big Data.<br><b>Impacto:</b> Aumento real da produtividade e diversificação do VAB.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">2: Zoneamento e Território</h4><p><b>Ação:</b> Zonas de Transição Tecnológica.<br><b>Como:</b> Revisão do Plano Diretor para criar "amortecedores" entre áreas residenciais e fábricas limpas.<br><b>Impacto:</b> Redução de conflitos urbanos e segurança jurídica.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">3: Retenção de Talentos</h4><p><b>Ação:</b> Hub de Inovação Industrial.<br><b>Como:</b> Parceria com a FATEC para qualificação técnica especializada.<br><b>Impacto:</b> Combate ao "Efeito Shadowing" e aumento da renda média.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">4: Servitização Industrial</h4><p><b>Ação:</b> Estímulo à Indústria como Serviço.<br><b>Como:</b> Apoio para grandes plantas incubarem startups de logística e manutenção preditiva.<br><b>Impacto:</b> Equilíbrio setorial e novas receitas tributárias.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">5: Atração de Investimentos e Empreendedorismo</h4><p><b>Ação:</b> Monitoramento Pós-IPCA.<br><b>Como:</b> Uso do Observatório para demonstrar ganhos reais de eficiência a investidores.<br><b>Impacto:</b> Melhoria da imagem municipal e competitividade.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">6: Evolução Setorial</h4><p><b>Ação:</b> Transição de alto nível tecnológico.<br><b>Como:</b> Transformar indústria tradicional em geradora de serviços avançados.<br><b>Impacto:</b> Sustentação do PIB a longo prazo.</p></div>', unsafe_allow_html=True)

elif menu == "Fontes/Referências":
    st.markdown('<p class="section-title">Fontes de Dados e Bibliografia</p>', unsafe_allow_html=True)
    col_ref, col_qr_ref = st.columns([0.6, 0.4])
    with col_ref:
        st.write("- **IBGE Cidades**: PIB Municipal e Valor Adicionado.")
        st.write("- **Fundação SEADE**: VAB Setorial.")
        st.write("- **Novo CAGED**: Movimentação formal de empregos.")
        st.write("- **Plano Diretor**: Lei Complementar 002/10.")
        st.write("- **BCB / IBGE**: IPCA.")
        st.write("- **Portal da Indústria / IEDI / ABDI**")
    with col_qr_ref:
        st.markdown('<div style="background:white; padding:20px; border-radius:12px; border:1px solid #e0e0e0; text-align:center;"><b>Material do Trabalho</b><p style="font-size:0.85rem; color:#666;">Acesse planilhas brutas no Drive:</p></div>', unsafe_allow_html=True)
        url_drive = "https://drive.google.com/drive/folders/12XwL_9c_lzHLopxX9lHEeNBGkn1old8G?usp=drive_link"
        st.image(gerar_qrcode(url_drive), width=180)
        st.link_button("📂 Abrir Pasta de Dados", url_drive, use_container_width=True)

# --- FOOTER ---
st.markdown('<div class="footer"><b>Observatório Industrial Votorantim | Inteligência Industrial 4.0</b><br>Grupo: Bruno V. Queiroz, Gislaine Takushi, Mariana Curvêlo, Victor Perillo e Vinicius Pierote.<br>Orientador: Flavianno A. de Lima</div>', unsafe_allow_html=True)
