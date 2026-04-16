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
    .highlight { color: #FF8C00; font-weight: bold; }
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

# --- FILTRAGEM DE DADOS PARA DISPLAY ---
if ano_selecionado == "Todos":
    display_df = df_hist.iloc[[-1]] 
    ano_txt = "2025 (Projeção)"
else:
    display_df = df_hist[df_hist['Ano'] == int(ano_selecionado)]
    ano_txt = ano_selecionado

dados_atuais = display_df.iloc[0]

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Contexto e Ordenamento Territorial</p>', unsafe_allow_html=True)
    
    tab_econ, tab_diretor = st.tabs(["📊 Análise Econômica", "📜 Plano Diretor de Votorantim"])
    
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
            Na prática, porém, o cenário atual cria dificuldades. As áreas industriais são limitadas e, com o crescimento da cidade, muitas delas passaram a ficar próximas ou até “encostadas” em regiões urbanas. Isso gera conflitos, pois aumenta a exigência por controle de impactos como ruído, trânsito de caminhões e poluição, restringindo principalmente a instalação de indústrias de maior porte.
            <br><br>
            Além disso, existem restrições ambientais importantes que reduzem ainda mais o espaço disponível, somadas a processos burocráticos e custos de adequação. O resultado é que, embora não haja proibição, há uma limitação prática: poucas áreas realmente viáveis e um nível alto de exigência para novos empreendimentos.
            <br><br>
            Em resumo, Votorantim permite a instalação de indústrias, mas o avanço urbano, as restrições ambientais e a escassez de zonas industriais adequadas tornam esse processo cada vez mais difícil, especialmente para empresas maiores ou com maior impacto.
            <br><br>
            <small>Fonte: <a href="https://www.votorantim.sp.gov.br/plano-diretor-lei-vigente-anexos" target="_blank">votorantim.sp.gov.br/plano-diretor</a></small>
        </div>
        """, unsafe_allow_html=True)

# --- 2. PROBLEMAS IDENTIFICADOS ---
elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("""**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes (como o Grupo Votorantim). 
Em termos de risco de negócio, isso é perigoso: se uma dessas verticais sofre um choque, o impacto no município é sistêmico.""")
        st.warning("""**Conflito Territorial:** O avanço do setor imobiliário sobre áreas industriais cria barreiras para a escalabilidade das fábricas. 
É um problema de Trade-off entre expansão urbana e manutenção da produção.""")
    with c2:
        st.error("""**Skill Gap (Mão de Obra):** Há um desalinhamento entre o perfil do trabalhador local e as demandas da Indústria 4.0. 
Enquanto o mercado pede automação, a força de trabalho ainda está atrelada a processos manuais.""")
        st.info("""**Efeito Shadowing:** Ocorre quando Votorantim perde talentos e investimentos para Sorocaba. 
Isso resulta em uma economia local estagnada, focada em setores de baixo valor agregado ou indústrias de base.""")

# --- 3. METODOLOGIA ETL ---
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

# --- 4. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    delta_yoy = None
    if ano_selecionado != "Todos":
        idx = df_hist[df_hist['Ano'] == int(ano_selecionado)].index[0]
        if idx > 0:
            pib_ant = df_hist.iloc[idx-1]['PIB']
            delta_yoy = f"{((dados_atuais['PIB']/pib_ant)-1)*100:.1f}% vs ano anterior"
    
    pib_2018 = df_hist.iloc[0]['PIB']
    perc_acumulado = ((dados_atuais['PIB']/pib_2018)-1)*100

    with c1:
        st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']), delta=delta_yoy)
        st.markdown(f'<p class="acumulado-text">🚀 Acumulado: <b>+{perc_acumulado:.1f}%</b> desde 2018</p>', unsafe_allow_html=True)
        
    with c2:
        st.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']))
    with c3:
        st.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']))
    with c4:
        st.metric("Produtividade", f"R$ {dados_atuais['Produtividade']}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist, x='Ano', y=['VAB_Industria', 'VAB_Servicos'],
                               title="Evolução Histórica: Indústria vs Serviços",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                               markers=True)
        fig_evolucao.update_xaxes(dtick=1)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">A linha de Serviços apresenta uma inclinação mais acentuada, indicando mudança no perfil econômico municipal.</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)

# --- 5. DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_hist, x='Ano', y='Produtividade', title="Produtividade (R$ / Operário)", color_discrete_sequence=['#1E3A8A'])
        fig_prod.update_xaxes(dtick=1)
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. PROJEÇÃO FUTURA ---
elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva de Cenários</p>', unsafe_allow_html=True)
    horizonte = st.radio("Selecione o Horizonte de Projeção:", ["Próximos 5 Anos (2028)", "Próximos 10 Anos (2033)"], horizontal=True)
    anos_a_projetar = 5 if "5" in horizonte else 10
    ano_final = 2023 + anos_a_projetar
    
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2026, ano_final + 1)

    def projetar_com_r2(y_hist):
        coef = np.polyfit(anos_hist, y_hist, 1)
        p = np.poly1d(coef)
        y_pred_hist = p(anos_hist)
        y_mean = np.mean(y_hist)
        ss_res = np.sum((y_hist - y_pred_hist) ** 2)
        ss_tot = np.sum((y_hist - y_mean) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        y_proj = p(anos_proj)
        return y_proj, r2

    proj_ind, r2_ind = projetar_com_r2(df_hist['VAB_Industria'].values)
    proj_serv, r2_serv = projetar_com_r2(df_hist['VAB_Servicos'].values)

    df_p = pd.DataFrame({
        'Ano': anos_proj, 
        f'VAB_Industria (R²={r2_ind:.3f})': proj_ind, 
        f'VAB_Servicos (R²={r2_serv:.3f})': proj_serv, 
        'Tipo': 'Projeção'
    })
    
    df_h_display = df_hist.rename(columns={
        'VAB_Industria': f'VAB_Industria (R²={r2_ind:.3f})',
        'VAB_Servicos': f'VAB_Servicos (R²={r2_serv:.3f})'
    })
    
    df_full = pd.concat([df_h_display.assign(Tipo='Histórico'), df_p])

    fig_proj = px.line(df_full, x='Ano', 
                      y=[f'VAB_Industria (R²={r2_ind:.3f})', f'VAB_Servicos (R²={r2_serv:.3f})'], 
                      color_discrete_map={
                          f'VAB_Industria (R²={r2_ind:.3f})': "#1E3A8A", 
                          f'VAB_Servicos (R²={r2_serv:.3f})': "#FF8C00"
                      },
                      line_dash='Tipo', title=f"Projeção de Crescimento até {ano_final} (Regressão Linear)")
    
    fig_proj.update_xaxes(dtick=1)
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.info(f"""
    **Estatísticas do Modelo:**
    * **Indústria:** $R^2 = {r2_ind:.4f}$ | Estimativa {ano_final}: R$ {proj_ind[-1]:.0f}M
    * **Serviços:** $R^2 = {r2_serv:.4f}$ | Estimativa {ano_final}: R$ {proj_serv[-1]:.0f}M
    """)

# --- 7. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)
    acoes = pd.DataFrame({
        "Problema Identificado": ["Dependência de Setor Único", "Efeito Shadowing (Sorocaba)", "Gap de Maturidade 4.0", "Crescimento de Serviços"],
        "Ação Estratégica": ["Verticalização da cadeia de minerais", "Incentivos para Startups de Logtech", "Subsídio para Auditoria Digital", "Estimular a Servitização Industrial"],
        "Impacto Esperado": ["Diversificação do VAB", "Retenção de Talentos", "Aumento da Produtividade", "Equilíbrio Setorial"]
    })
    st.table(acoes)
    st.markdown("> **Nota do Grupo:** Este plano visa transformar Votorantim em um hub de inteligência industrial.")

# --- 8. FONTES/REFERÊNCIAS ---
elif menu == "Fontes/Referências":
    st.markdown('<p class="section-title">Fontes de Dados</p>', unsafe_allow_html=True)
    st.write("- IBGE Cidades (PIB Municipal)")
    st.write("- Fundação SEADE (VAB Setorial Municipal)")
    st.write("- Novo CAGED (Movimentação de Emprego Formal)")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <b>Observatório Industrial Votorantim | Ciência de Dados para Negócio</b><br>
        Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.<br>
        <i>Gerado em {datetime.now().strftime('%d/%m/%Y')}</i>
    </div>
    """, unsafe_allow_html=True)
