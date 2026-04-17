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

# Mapa de IPCA Histórico
ipca_map = {2018: 3.75, 2019: 4.31, 2020: 4.52, 2021: 10.06, 2022: 5.79, 2023: 4.62, 2024: 4.50, 2025: 4.00}

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
        </div>
        """, unsafe_allow_html=True)
    with tab_diretor:
        st.markdown("""
        <div class="card">
            Votorantim possui um <b>Plano Diretor</b> que organiza o crescimento da cidade... o avanço urbano e as restrições ambientais tornam o processo industrial cada vez mais difícil.
        </div>
        """, unsafe_allow_html=True)

# --- 2. PROBLEMAS IDENTIFICADOS ---
elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes.")
        st.warning("**Conflito Territorial:** Avanço imobiliário sobre áreas industriais.")
    with c2:
        st.error("**Skill Gap (Mão de Obra):** Desalinhamento com a Indústria 4.0.")
        st.info("**Efeito Shadowing:** Perda de talentos para Sorocaba.")

# --- 3. METODOLOGIA ETL ---
elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    st.markdown('<div class="step-box step-extracao"><b>1. Extração:</b> Dados brutos de IBGE, SEADE e CAGED.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box step-transformacao"><b>2. Transformação:</b> Limpeza e padronização CNAE.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box step-carga"><b>3. Carregamento:</b> Exportação para formatos Streamlit.</div>', unsafe_allow_html=True)

# --- 4. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']))
    with c2: st.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']))
    with c3: st.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']))
    with c4: st.metric("Produtividade", f"R$ {dados_atuais['Produtividade']}k")

    # Botão IPCA existente no Dashboard
    st.markdown("---")
    if "aplicar_ipca_dash" not in st.session_state: st.session_state.aplicar_ipca_dash = False
    if st.button("Inserir IPCA (Impacto Inflacionário Histórico)"):
        st.session_state.aplicar_ipca_dash = not st.session_state.aplicar_ipca_dash

    df_plot = df_hist.copy()
    if st.session_state.aplicar_ipca_dash:
        df_plot['Fator'] = [(np.prod([(1 + ipca_map[y]/100) for y in ipca_map if y <= ano])) for ano in df_plot['Ano']]
        df_plot['Indústria (Real)'] = df_plot['VAB_Industria'] / df_plot['Fator']
        df_plot['Serviços (Real)'] = df_plot['VAB_Servicos'] / df_plot['Fator']
        y_cols = ['VAB_Industria', 'Indústria (Real)', 'VAB_Servicos', 'Serviços (Real)']
    else:
        y_cols = ['VAB_Industria', 'VAB_Servicos']

    st.plotly_chart(px.line(df_plot, x='Ano', y=y_cols, title="Crescimento Histórico Nominal vs Real"), use_container_width=True)

# --- 5. DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.bar(df_hist, x='Ano', y='Produtividade', title="Produtividade (R$ / Operário)"), use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself'))
        fig_radar.update_layout(title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. PROJEÇÃO FUTURA (SOLICITAÇÃO: IPCA PREVISIONADO + EXTENSÃO 2035) ---
elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva e Previsão de IPCA</p>', unsafe_allow_html=True)
    
    horizonte = st.radio("Selecione o Horizonte de Projeção:", ["Próximos 5 Anos (2030)", "Próximos 10 Anos (2035)"], horizontal=True)
    anos_a_projetar = 5 if "5" in horizonte else 10
    ano_final = 2025 + anos_a_projetar
    
    anos_hist = df_hist['Ano'].values
    anos_proj = np.arange(2026, ano_final + 1)

    # Função Regressão
    def projetar_com_r2(x_hist, y_hist, x_proj):
        coef = np.polyfit(x_hist, y_hist, 1)
        p = np.poly1d(coef)
        y_proj = p(x_proj)
        y_pred_hist = p(x_hist)
        r2 = 1 - (np.sum((y_hist - y_pred_hist) ** 2) / np.sum((y_hist - np.mean(y_hist)) ** 2))
        return y_proj, r2, p

    # Projeções de VAB
    proj_ind, r2_ind, model_ind = projetar_com_r2(anos_hist, df_hist['VAB_Industria'].values, anos_proj)
    proj_serv, r2_serv, model_serv = projetar_com_r2(anos_hist, df_hist['VAB_Servicos'].values, anos_proj)

    # --- NOVIDADE: PREVISÃO DE IPCA POR REGRESSÃO ---
    anos_ipca = np.array(list(ipca_map.keys()))
    valores_ipca = np.array(list(ipca_map.values()))
    proj_ipca_val, r2_ipca, model_ipca = projetar_com_r2(anos_ipca, valores_ipca, anos_proj)
    
    st.sidebar.markdown("---")
    if "aplicar_deflacao_proj" not in st.session_state: st.session_state.aplicar_deflacao_proj = False
    
    # Botão de aplicar IPCA na Projeção
    if st.button("Aplicar IPCA Previsionado (Ver Crescimento Real Projetado)"):
        st.session_state.aplicar_deflacao_proj = not st.session_state.aplicar_deflacao_proj

    # Construção do DataFrame de Projeção
    df_proj_total = pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': proj_ind, 'VAB_Servicos': proj_serv, 'IPCA_Previsto': proj_ipca_val, 'Tipo': 'Projeção'})
    
    if st.session_state.aplicar_deflacao_proj:
        st.warning(f"📉 Analisando Crescimento Real: IPCA futuro médio previsto por regressão: {np.mean(proj_ipca_val):.2f}% ao ano.")
        # Fator acumulado histórico até 2025
        fator_2025 = np.prod([(1 + v/100) for v in ipca_map.values()])
        # Fator futuro acumulado
        fatores_futuros = [fator_2025 * np.prod([(1 + v/100) for v in proj_ipca_val[:i+1]]) for i in range(len(proj_ipca_val))]
        df_proj_total['Indústria (Real)'] = df_proj_total['VAB_Industria'] / fatores_futuros
        df_proj_total['Serviços (Real)'] = df_proj_total['VAB_Servicos'] / fatores_futuros
        y_cols_proj = ['VAB_Industria', 'Indústria (Real)', 'VAB_Servicos', 'Serviços (Real)']
    else:
        y_cols_proj = ['VAB_Industria', 'VAB_Servicos']

    df_full_proj = pd.concat([df_hist.assign(Tipo='Histórico'), df_proj_total])
    
    fig_proj = px.line(df_full_proj, x='Ano', y=y_cols_proj, 
                      line_dash='Tipo', title=f"Projeção Econômica Votorantim até {ano_final}",
                      color_discrete_map={"VAB_Industria": "#1E3A8A", "Indústria (Real)": "#93c5fd", "VAB_Servicos": "#FF8C00", "Serviços (Real)": "#fdba74"})
    
    fig_proj.update_xaxes(dtick=1, range=[2018, ano_final + 0.5])
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.info(f"""
    **Estatísticas do Modelo:**
    * **Indústria:** $R^2 = {r2_ind:.4f}$ | Est. {ano_final}: R$ {proj_ind[-1]:.0f}M
    * **Serviços:** $R^2 = {r2_serv:.4f}$ | Est. {ano_final}: R$ {proj_serv[-1]:.0f}M
    * **IPCA Previsionado (Regressão):** $R^2 = {r2_ipca:.4f}$ | Tendência: {"Queda" if model_ipca.coef[0] < 0 else "Alta"}
    """)

# --- 7. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)
    acoes = pd.DataFrame({
        "Problema": ["Dependência Setorial", "Efeito Shadowing", "Gap 4.0"],
        "Ação": ["Verticalização Mineral", "Incentivos Logtech", "Auditoria Digital"],
        "Impacto": ["Diversificação", "Retenção de Talentos", "Produtividade"]
    })
    st.table(acoes)

# --- 8. FONTES/REFERÊNCIAS ---
elif menu == "Fontes/Referências":
    st.markdown('<p class="section-title">Fontes de Dados</p>', unsafe_allow_html=True)
    st.write("- IBGE Cidades | SEADE | Novo CAGED | Plano Diretor | IPCA Histórico IBGE")

# --- FOOTER ---
st.markdown(f'<div class="footer">Observatório Industrial Votorantim | Gerado em {datetime.now().strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
