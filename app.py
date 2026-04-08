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
    st.title("Inteligência Industrial")
    st.subheader("Votorantim 4.0")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Introdução & Contexto", "Metodologia ETL", "Dashboard Executivo", 
                    "Diagnóstico Indústria 4.0", "Projeção Futura", "Plano de Ação", "Fontes/Referências"])

# Lógica de Dados para Gráficos
if ano_selecionado == "Todos":
    df_plot = df_hist
    display_df = df_hist.iloc[[-1]] 
else:
    # Mantemos o histórico para o gráfico não quebrar, mas destacamos o ano
    df_plot = df_hist
    display_df = df_hist[df_hist['Ano'] == int(ano_selecionado)]

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Análise de Contexto Econômico</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        Votorantim ainda carrega um legacy industrial muito forte, focado em indústria de base (cimento e metalurgia). 
        No entanto, o dataset econômico da cidade mostra uma transição clara: a indústria está perdendo share no PIB para o setor de Serviços, 
        o que indica um processo de desindustrialização ou mudança de matriz econômica. O cenário sugere que Votorantim vive um efeito de 
        "Shadowing" de Sorocaba. Enquanto a vizinha atrai indústrias de alto valor agregado (Tech e Automotiva), Votorantim fica com o setor 
        de baixo valor agregado e alto impacto ambiental.
        <br><br>
        <span class="highlight">Destaque:</span> A proximidade com o polo tecnológico de Sorocaba cria um desafio de retenção de talentos e 
        necessidade de modernização para que Votorantim não se torne apenas um fornecedor de baixo valor agregado.
        <br><br>
        <span class="highlight">Insight:</span> Para reverter isso, o município precisaria de políticas de incentivo baseadas em predição 
        de demanda tecnológica e uma atualização urgente no currículo técnico da população para atrair empresas que gerem mais dados e menos poeira.
    </div>
    """, unsafe_allow_html=True)
    
  st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.error("""**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes (como o Grupo Votorantim). 
Em termos de risco de negócio, isso é perigoso: se uma dessas verticais sofre um choque, o impacto no município é sistêmico.""")
    
    st.warning("""**Conflito Territorial:** O avanço do setor imobiliário sobre áreas industriais cria barreiras para a escalabilidade das fábricas. 
É um problema de Trade-off entre expansão urbana e manutenção da produção. 
Enquanto o mercado pede automação e análise de dados, a força de trabalho ainda está muito atrelada a processos manuais/analógicos.""")

with c2:
    st.error("**Skill Gap (Mão de Obra):** Baixa digitalização em pequenas e médias empresas.")
    st.info("**Efeito Shadowing:** Fuga de capital intelectual para Sorocaba.")

# --- 2. METODOLOGIA ETL ---
elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="step-box">
            <b>1. Extração:</b> 
            Ação: Coletamos dados brutos de três fontes governamentais distintas: IBGE Cidades (Séries históricas de PIB), SEADE (VAB por setor municipal) e Novo CAGED (Movimentação formal de empregos).
            Formatos: Os dados foram extraídos originalmente em formatos como CSV (tabelas de emprego) e XML/JSON (via APIs ou consultas em tabelas do SIDRA/IBGE).
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="step-box">
            <b>2. Transformação:</b> 
            Limpeza de Nulos: Removemos registros incompletos de anos onde o IBGE ainda não consolidou o PIB (lembrando que o PIB municipal tem um lag de 2 anos).
            Padronização de Nomenclaturas: Unificamos as classificações. O que no CAGED estava como "CNAE 2.3 - Fabricação de Cimento", no SEADE agrupamos como "Indústria de Minerais Não Metálicos" para garantir a integridade da análise.
            Unificação (Join): Realizamos o merge das bases de Emprego e PIB utilizando o Ano e o Código de Município do IBGE como chaves primárias, criando um dataset único e consistente para os gráficos.
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="step-box">
            <b>3. Carga:</b> 
            Ação: O dataset limpo foi estruturado em DataFrames (Pandas) e exportado para formatos prontos para consumo (.csv), permitindo a visualização imediata através de bibliotecas de plotagem (Plotly/Matplotlib) no Vs.Code.
            Armazenamento em DataFrames estruturados para visualização dinâmica no Streamit.
        </div>
    ''', unsafe_allow_html=True)

# --- 3. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    vab_i = display_df['VAB_Industria'].values[0]
    vab_s = display_df['VAB_Servicos'].values[0]
    
    c1.metric("VAB Indústria", f"R$ {vab_i:,.2f} Mi", delta=None if ano_selecionado == "Todos" else f"{vab_i - df_hist.iloc[0]['VAB_Industria']:.1f} cresc. total")
    c2.metric("VAB Serviços", f"R$ {vab_s:,.2f} Mi")
    c3.metric("Produtividade", f"R$ {display_df['Produtividade'].values[0]}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        # Gráfico que não "some": mostra a linha e destaca o ano selecionado
        fig_evolucao = px.line(df_plot, x='Ano', y=['VAB_Industria', 'VAB_Servicos'],
                               title="Evolução Histórica: Indústria vs Serviços",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                               markers=True)
        
        if ano_selecionado != "Todos":
            fig_evolucao.add_selection(x=[int(ano_selecionado)]) # Destaque visual
            
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">A linha de Serviços apresenta uma inclinação mais acentuada, indicando mudança no perfil econômico municipal.</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)

# --- 4. DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_plot, x='Ano', y='Produtividade', title="Produtividade (R$ / Operário)", color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 5. PROJEÇÃO FUTURA ---
elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva de Cenários</p>', unsafe_allow_html=True)
    
    horizonte = st.radio("Selecione o Horizonte de Projeção:", ["Próximos 5 Anos (2028)", "Próximos 10 Anos (2033)"], horizontal=True)
    anos_a_projetar = 5 if "5" in horizonte else 10
    ano_final = 2023 + anos_a_projetar
    
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2024, ano_final + 1)
    
    def projetar(valores, n_anos):
        coef = np.polyfit(anos_hist, valores, 1)
        futuro = np.arange(2024, 2024 + n_anos)
        return np.polyval(coef, futuro)

    proj_ind = projetar(df_hist['VAB_Industria'].values, anos_a_projetar)
    proj_serv = projetar(df_hist['VAB_Servicos'].values, anos_a_projetar)

    df_proj = pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': proj_ind, 'VAB_Servicos': proj_serv, 'Tipo': 'Projeção'})
    df_completo = pd.concat([df_hist.assign(Tipo='Histórico'), df_proj])

    fig_proj = px.line(df_completo, x='Ano', y=['VAB_Industria', 'VAB_Servicos'], 
                      color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                      line_dash='Tipo', title=f"Projeção de Crescimento até {ano_final}")
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.info(f"Estimativa para {ano_final}: Indústria R$ {proj_ind[-1]:.0f}M | Serviços R$ {proj_serv[-1]:.0f}M")

# --- 6. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)
    
    # Plano de ação focado nos problemas reais identificados na introdução e dashboard
    acoes_corrigidas = pd.DataFrame({
        "Problema Identificado": [
            "Dependência de Setor Único (Minerais)",
            "Efeito Shadowing (Sorocaba)",
            "Gap de Maturidade 4.0",
            "Crescimento Acelerado de Serviços"
        ],
        "Ação Estratégica": [
            "Verticalização da cadeia de minerais para produtos de alto valor (ex: cerâmica técnica).",
            "Criação de Incentivos para Instalação de Startups de 'Logtech' e 'Industrial IoT'.",
            "Programa Municipal de Subsídio para Auditoria de Maturidade Digital em PMEs.",
            "Estimular a 'Servitização' industrial (Indústrias vendendo serviços e dados)."
        ],
        "Impacto Esperado": ["Diversificação do VAB", "Retenção de Talentos", "Aumento da Produtividade", "Equilíbrio Setorial"]
    })
    
    st.table(acoes_corrigidas)
    
    st.markdown("""
    > **Nota do Grupo:** Este plano visa utilizar os insights extraídos (crescimento de serviços e alta produtividade industrial) 
    > para transformar Votorantim em um hub de inteligência industrial, e não apenas uma base extrativista.
    """)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <b>Observatório Industrial Votorantim | Ciência de Dados para Negócio</b><br>
        Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.<br>
        <i>Gerado em {datetime.now().strftime('%d/%m/%Y')}</i>
    </div>
    """, unsafe_allow_html=True)
