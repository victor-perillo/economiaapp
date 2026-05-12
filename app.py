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
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* Cards Brancos Estilizados */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    /* Títulos de Seção */
    .section-title {
        color: #1e3a8a;
        font-size: 2rem;
        font-weight: 700;
        border-left: 10px solid #ff8c00;
        padding-left: 20px;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    /* ETL Steps */
    .step-box { 
        padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 8px solid; 
    }
    .step-extracao { background-color: #eff6ff; border-color: #1e3a8a; color: #1e3a8a; }
    .step-transformacao { background-color: #fffaf5; border-color: #ff8c00; color: #854d0e; }
    .step-carga { background-color: #f0fdf4; border-color: #22c55e; color: #166534; }

    /* Zoneamento Cards */
    .z-card { 
        background-color: #f1f5f9; padding: 1.2rem; border-radius: 8px; 
        border-left: 5px solid #ff8c00; margin-bottom: 12px; min-height: 100px;
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] { background-color: #0f172a; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* Utilitários */
    .chart-caption { text-align: center; color: #64748b; font-style: italic; margin-top: 8px; font-size: 0.9rem; }
    .footer {
        text-align: center; padding: 3rem; color: #64748b; font-size: 0.9rem;
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

# --- MÓDULO: INTRODUÇÃO E CONTEXTO ---
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
        pdf_url = "https://www.votorantim.sp.gov.br/arquivos/mapas_002_19043716.pdf"
        st.link_button("🔍 Abrir Mapa de Zoneamento", pdf_url, use_container_width=True)

# --- MÓDULO: PROBLEMAS IDENTIFICADOS ---
elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("""**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes (como o Grupo Votorantim). 
        Em termos de risco de negócio, isso é perigoso: se uma dessas verticais sofre um choque, o impacto no município é sistêmico.""")
        st.warning("""**Conflito Territorial:** O avanço do setor imobiliário sobre áreas industriais cria barreiras para a escalabilidade das fábricas. 
        É um problema de Trade-off entre expansão urbana e manutenção da produção.""")
    with c2:
        st.success("""**Evolução Setorial:** Apesar de ser um sinal de modernização, o risco é a desindustrialização precoce. Se a indústria enfraquecer rápido demais e o setor de serviços for apenas de 'baixo valor agregado' (como pequenos comércios ou serviços básicos), a renda média da cidade cai.""")
        st.info("""**Efeito Shadowing:** Ocorre quando Votorantim perde talentos e investimentos para Sorocaba. 
        Isso resulta em uma economia local estagnada, focada em setores de baixo valor agregado.""")

# --- MÓDULO: METODOLOGIA ETL ---
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

# --- MÓDULO: DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3) 
    
    with c1: st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']))
    with c2: st.metric("VAB Indústria (Est.)", formatar_valor(dados_atuais['VAB_Industria']))
    with c3: st.metric("VAB Serviços (Est.)", formatar_valor(dados_atuais['VAB_Servicos']))

    st.markdown("---")
    
    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB'], name='PIB Votorantim Corrente', marker_color='#1E3A8A'))
    fig_comparativo.add_trace(go.Bar(x=df_hist['Ano'], y=df_hist['PIB_Constante'], name='PIB Constante (2023)', marker_color='#E67E22'))
    fig_comparativo.update_layout(
        title="Evolução do PIB (Correntes vs Constantes de 2023), em R$ mil",
        xaxis_title="Ano", barmode='group', legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig_comparativo, use_container_width=True)

    if "aplicar_ipca_dash" not in st.session_state: st.session_state.aplicar_ipca_dash = False
    if st.button("Inserir IPCA (Impacto Inflacionário Histórico até 2023)"):
        st.session_state.aplicar_ipca_dash = not st.session_state.aplicar_ipca_dash

    df_p = df_hist.copy() 
    if st.session_state.aplicar_ipca_dash:
        ipca_filtered = {k: v for k, v in ipca_map.items() if k <= 2023}
        df_p['Fator'] = [(np.prod([(1 + ipca_filtered[y]/100) for y in ipca_filtered if y <= ano])) for ano in df_p['Ano']]
        df_p['Indústria (Real)'] = df_p['VAB_Industria'] / df_p['Fator']
        df_p['Serviços (Real)'] = df_p['VAB_Servicos'] / df_p['Fator']
        y_cols = ['VAB_Industria', 'Indústria (Real)', 'VAB_Servicos', 'Serviços (Real)']
    else:
        y_cols = ['VAB_Industria', 'VAB_Servicos']

    col_left, col_right = st.columns([0.65, 0.35])
    with col_left:
        fig_evolucao = px.line(df_p, x='Ano', y=y_cols, title="Evolução Histórica: Indústria vs Serviços", markers=True,
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "Indústria (Real)": "#93c5fd", "VAB_Servicos": "#FF8C00", "Serviços (Real)": "#fdba74"})
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">A análise revela que o PIB cresceu nominalmente de R$ 670 Mi em 2002 para R$ 5.2 Bi em 2023. O pico real em 2014 sugere uma expansão industrial atípica no período.</div>', unsafe_allow_html=True)
    with col_right:
        st.write("**Referência IPCA Aplicada (até 2023):**")
        ipca_exec_tab = pd.DataFrame([(k, v) for k, v in ipca_map.items() if k <= 2023], columns=['Ano', 'IPCA (%)'])
        st.dataframe(ipca_exec_tab, hide_index=True, height=250)
        st.plotly_chart(px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE"), use_container_width=True)

# --- MÓDULO: DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Geração Digital e Impactos 4.0</p>', unsafe_allow_html=True)
    st.warning("""
        **Nota de Transparência:** As projeções de crescimento com Indústria 4.0 apresentadas abaixo utilizam como referência uma **média nacional** de ganhos de eficiência. 
        O gráfico de 'Nível de Automação' é mensurado com base no **número de CNAEs** ativos em Votorantim. 
        Fontes: ibge.gov.br; portaldaindustria.com.br; iedi.org.br; abdi.com.br
    """)

    st.markdown("""
    <div class="card">
        <h3 style="color: #1E3A8A;">A Revolução 4.0 em Votorantim</h3>
        <p>A <b>Indústria 4.0</b> integra tecnologias digitais como IoT, Big Data e IA ao chão de fábrica. Em nível nacional, a adesão a esse modelo está transformando plantas tradicionais em <b>Fábricas Inteligentes</b>.</p>
        <div style="display: flex; gap: 15px;">
            <div class="z-card" style="flex:1;"><b>Ganho de Eficiência:</b> Sensores em tempo real reduzem desperdícios nas indústrias de base.</div>
            <div class="z-card" style="flex:1;"><b>Manutenção Preditiva:</b> Algoritmos preveem falhas antes de paradas caras na produção.</div>
            <div class="z-card" style="flex:1;"><b>Customização:</b> Flexibilidade para atender demandas específicas com menor custo.</div>
        </div>
        <p style="margin-top:15px;"><b>Como está acontecendo:</b> Empresas locais investem na digitalização e na qualificação técnica, elevando a competitividade do VAB municipal frente a outros hubs.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: 
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=['Sem Tecnologia 4.0', 'Com Tecnologia 4.0'], y=[210, 345], marker_color=['#94a3b8', '#FF8C00'], text=['R$ 210k', 'R$ 345k'], textposition='auto'))
        fig_comp.add_hline(y=280, line_dash="dash", line_color="red", annotation_text="Média Nacional: R$ 280k")
        fig_comp.update_layout(title="Diferença de Produtividade: +35% com Indústria 4.0", yaxis_title="R$ / Operário (Milhares)", showlegend=False)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.info("O percentual de diferença entre empresas tecnológicas e tradicionais é de **35%**, superando a média nacional em **R$ 65k** por operário.")
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- MÓDULO: PROJEÇÃO FUTURA ---
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
        st.session_state.deflacao_proj = not st.session_state.get('deflacao_proj', False)

    df_p_total = pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': p_ind, 'VAB_Servicos': p_serv, 'Tipo': 'Projeção'})
    if st.session_state.get('deflacao_proj', False):
        st.info("A queda ocorre porque estamos descontando a inflação futura. Sem inovação tecnológica, a riqueza real será corroída.")
        f_2023 = np.prod([(1 + v/100) for v in ipca_map.values() if v > 0])
        fatores = [f_2023 * np.prod([(1 + v/100) for v in p_ipca[:i+1]]) for i in range(len(p_ipca))]
        df_p_total['Indústria (Real)'] = df_p_total['VAB_Industria'] / fatores
        df_p_total['Serviços (Real)'] = df_p_total['VAB_Servicos'] / fatores
        y_cols_p = ['VAB_Industria', 'Indústria (Real)', 'VAB_Servicos', 'Serviços (Real)']
    else:
        y_cols_p = ['VAB_Industria', 'VAB_Servicos']

    df_f = pd.concat([df_hist.assign(Tipo='Histórico'), df_p_total])
    st.plotly_chart(px.line(df_f, x='Ano', y=y_cols_p, line_dash='Tipo', title="Projeção Econômica até 2030", 
                            color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"}), use_container_width=True)
    st.info(f"**Estatísticas:** Indústria $R^2$: {r2_ind:.4f} | Serviços $R^2$: {r2_serv:.4f} | IPCA Médio Previsto: {np.mean(p_ipca):.2f}%")

# --- MÓDULO: PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">1: Modernização Industrial</h4><p><b>Ação:</b> Programa Votorantim 4.0.<br><b>Como:</b> Isenção parcial de ISS/IPTU para empresas que investirem em IoT e Big Data.<br><b>Impacto:</b> Aumento real da produtividade e diversificação do VAB.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">2: Zoneamento e Território</h4><p><b>Ação:</b> Zonas de Transição Tecnológica.<br><b>Como:</b> Revisão do Plano Diretor para criar "amortecedores" entre áreas residenciais e fábricas limpas.<br><b>Impacto:</b> Redução de conflitos urbanos e segurança jurídica.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">3: Retenção de Talentos</h4><p><b>Ação:</b> Hub de Inovação Industrial.<br><b>Como:</b> Parceria com a FATEC para qualificação técnica especializada.<br><b>Impacto:</b> Combate ao "Efeito Shadowing" e aumento da renda média.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">4: Servitização Industrial</h4><p><b>Ação:</b> Estímulo à Indústria como Serviço.<br><b>Como:</b> Apoio para grandes plantas incubarem startups de logística e manutenção preditiva.<br><b>Impacto:</b> Equilíbrio setorial e novas receitas tributárias.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">5: Atração de Investimentos</h4><p><b>Ação:</b> Monitoramento Pós-IPCA.<br><b>Como:</b> Uso do Observatório para demonstrar ganhos reais de eficiência a investidores.<br><b>Impacto:</b> Melhoria da imagem municipal e competitividade.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4 style="color: #1E3A8A;">6: Evolução Setorial</h4><p><b>Ação:</b> Transição de alto nível tecnológico.<br><b>Como:</b> Transformar indústria tradicional em geradora de serviços avançados.<br><b>Impacto:</b> Sustentação do PIB a longo prazo.</p></div>', unsafe_allow_html=True)

# --- MÓDULO: FONTES ---
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
st.markdown('<div class="footer"><b>Observatório Industrial Votorantim | Inteligência Industrial 4.0</b><br>Grupo: Bruno V. Queiroz, Gislaine Takushi, Mariana Curvêlo, Victor Perillo e Vinicius Pierote.</div>', unsafe_allow_html=True)
