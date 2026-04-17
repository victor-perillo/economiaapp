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

# --- CONTEÚDO ---
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
            Votorantim possui um <b>Plano Diretor</b> que organiza o crescimento da cidade e define onde atividades industriais podem se instalar, sempre respeitando regras de uso do solo e exigências ambientais.
            <br><br>
            Em resumo, Votorantim permite a instalação de indústrias, mas o avanço urbano, as restrições ambientais e a escassez de zonas industriais adequadas tornam esse processo cada vez mais difícil, especialmente para empresas maiores ou com maior impacto.
        </div>
        """, unsafe_allow_html=True)

elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes.")
    with c2:
        st.info("**Efeito Shadowing:** Ocorre quando Votorantim perde talentos para Sorocaba.")

elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']))
    with c2: st.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']))
    with c3: st.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']))
    with c4: st.metric("Produtividade", f"R$ {dados_atuais['Produtividade']}k")

    # --- LÓGICA DO IPCA COM TABELA DE REFERÊNCIA PARA APRESENTAÇÃO ---
    st.markdown("---")
    if "mostrar_ipca" not in st.session_state:
        st.session_state.mostrar_ipca = False

    if st.button("Inserir IPCA"):
        st.session_state.mostrar_ipca = True

    if st.session_state.mostrar_ipca:
        ipca_data = {
            2018: 3.75, 2019: 4.31, 2020: 4.52, 2021: 10.06, 
            2022: 5.79, 2023: 4.62, 2024: 4.50, 2025: 4.00
        }
        df_ipca = pd.DataFrame(list(ipca_data.items()), columns=['Ano', 'IPCA (%)'])

        col_inf, col_tab = st.columns([0.6, 0.4])

        with col_inf:
            if ano_selecionado == "Todos":
                acumulado = (np.prod([(1 + v/100) for v in ipca_data.values()]) - 1) * 100
                st.metric("IPCA Acumulado do Período", f"{acumulado:.2f}%")
                fig_ipca = px.bar(df_ipca, x='Ano', y='IPCA (%)', title="Evolução do IPCA (%)", color_discrete_sequence=['#FF8C00'], text_auto='.2f')
            else:
                valor_ano = ipca_data.get(int(ano_selecionado), 0)
                st.metric(f"IPCA ({ano_selecionado})", f"{valor_ano}%")
                df_ipca['Destaque'] = df_ipca['Ano'].apply(lambda x: 'Selecionado' if x == int(ano_selecionado) else 'Outros')
                fig_ipca = px.bar(df_ipca, x='Ano', y='IPCA (%)', color='Destaque', title=f"Foco IPCA: {ano_selecionado}",
                                 color_discrete_map={'Selecionado': '#FF8C00', 'Outros': '#1E3A8A'}, text_auto='.2f')
            st.plotly_chart(fig_ipca, use_container_width=True)

        with col_tab:
            st.markdown("**Referência para Apresentação:**")
            st.dataframe(df_ipca[['Ano', 'IPCA (%)']], hide_index=True, use_container_width=True)
            st.caption("Valores considerados para deflação e análise de crescimento real.")
            
    st.markdown("---")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist, x='Ano', y=['VAB_Industria', 'VAB_Servicos'],
                               title="Evolução Histórica: Indústria vs Serviços",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"}, markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)

elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)

elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva de Cenários</p>', unsafe_allow_html=True)

elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico Condizente</p>', unsafe_allow_html=True)

elif menu == "Fontes/Referências":
    st.markdown('<p class="section-title">Fontes de Dados</p>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f'<div class="footer"><b>Observatório Industrial Votorantim</b><br>Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</div>', unsafe_allow_html=True)
