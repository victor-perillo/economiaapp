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
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---
def formatar_valor(valor):
    """Converte valores numéricos para string formatada em Mi ou Bi"""
    if valor >= 1000:
        return f"R$ {valor/1000:.2f} Bi"
    return f"R$ {valor:.1f} Mi"

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    # Dados de Segmentos (Diagnóstico)
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Papel e Celulose", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [48, 18, 15, 10, 6, 3],
        'Dificuldade_40': [65, 55, 40, 50, 80, 45], 
        'Maturidade_Atual': [2.8, 3.2, 3.5, 2.9, 1.8, 2.4] 
    })
    
    # Séries Históricas baseadas no CSV e Projeções
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
    
    anos_disponiveis = [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Período de Análise:", anos_disponiveis, index=len(anos_disponiveis)-3) # Default 2023
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Introdução & Contexto", "Problemas Identificados", "Metodologia ETL", 
                    "Dashboard Executivo", "Diagnóstico Indústria 4.0", "Projeção Futura", 
                    "Plano de Ação", "Fontes/Referências"])

# --- FILTRAGEM DE DADOS ---
dados_ano = df_hist[df_hist['Ano'] == int(ano_selecionado)].iloc[0]
idx_ano = df_hist[df_hist['Ano'] == int(ano_selecionado)].index[0]

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Análise de Contexto Econômico</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        Votorantim ainda carrega um legacy industrial muito forte, focado em indústria de base (cimento e metalurgia). 
        No entanto, os dados de <b>{ano_selecionado}</b> mostram uma transição clara: o setor de Serviços (<b>{formatar_valor(dados_ano['VAB_Servicos'])}</b>) 
        já supera significativamente a Indústria (<b>{formatar_valor(dados_ano['VAB_Industria'])}</b>).
        <br><br>
        O cenário sugere que Votorantim vive um efeito de <b>"Shadowing"</b> de Sorocaba, integrando-se como polo de serviços regional.
    </div>
    """, unsafe_allow_html=True)

# --- 2. PROBLEMAS IDENTIFICADOS ---
elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Clusterização**: Dependência de poucos players gigantes.")
        st.warning("**Conflito Territorial**: Expansão urbana vs áreas industriais.")
    with c2:
        st.error("**Skill Gap**: Mão de obra desalinhada com Automação 4.0.")
        st.info("**Efeito Shadowing**: Vazamento de talentos e impostos para Sorocaba.")

# --- 3. METODOLOGIA ETL ---
elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="step-box step-extracao"><b>1. Extração:</b> Coleta de dados via IBGE Cidades e SEADE.</div>
        <div class="step-box step-transformacao"><b>2. Transformação:</b> Limpeza no Pandas e unificação de escalas (Mi para Bi).</div>
        <div class="step-box step-carga"><b>3. Carregamento:</b> Estruturação para visualização no Streamlit.</div>
    ''', unsafe_allow_html=True)

# --- 4. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    # Cards Dinâmicos
    c1, c2, c3, c4 = st.columns(4)
    
    delta_pib = None
    if idx_ano > 0:
        pib_ant = df_hist.iloc[idx_ano-1]['PIB']
        delta_pib = f"{((dados_ano['PIB']/pib_ant)-1)*100:.1f}%"

    with c1:
        st.metric("PIB Municipal", formatar_valor(dados_ano['PIB']), delta=delta_pib)
    with c2:
        st.metric("VAB Indústria", formatar_valor(dados_ano['VAB_Industria']))
    with c3:
        st.metric("VAB Serviços", formatar_valor(dados_ano['VAB_Servicos']))
    with c4:
        st.metric("Produtividade", f"R$ {dados_ano['Produtividade']}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist, x='Ano', y=['VAB_Industria', 'VAB_Servicos', 'PIB'],
                               title="Evolução Econômica: PIB vs Setores",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00", "PIB": "#2b8a3e"},
                               markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)

    with col_right:
        fig_pizza = px.pie(values=[dados_ano['VAB_Industria'], dados_ano['VAB_Servicos']], 
                          names=['Indústria', 'Serviços'], hole=.4, 
                          title=f"Mix de Riqueza ({ano_selecionado})",
                          color_discrete_sequence=["#1E3A8A", "#FF8C00"])
        st.plotly_chart(fig_pizza, use_container_width=True)

# --- 5. DIAGNÓSTICO INDÚSTRIA 4.0 ---
elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_hist, x='Ano', y='Produtividade', title="Produtividade (R$ / Operário)", color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. PROJEÇÃO FUTURA ---
elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva de Cenários</p>', unsafe_allow_html=True)
    anos_proj = np.arange(2026, 2031)
    
    def projetar(valores):
        coef = np.polyfit(df_hist['Ano'], valores, 1)
        return np.polyval(coef, anos_proj)

    df_p = pd.DataFrame({'Ano': anos_proj, 'VAB_Industria': projetar(df_hist['VAB_Industria']), 'VAB_Servicos': projetar(df_hist['VAB_Servicos'])})
    df_full = pd.concat([df_hist, df_p])
    
    fig_proj = px.line(df_full, x='Ano', y=['VAB_Industria', 'VAB_Servicos'], title="Tendência 2030",
                       color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"})
    st.plotly_chart(fig_proj, use_container_width=True)

# --- 7. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano Estratégico 2026</p>', unsafe_allow_html=True)
    acoes = pd.DataFrame({
        "Ação": ["Verticalização de Minerais", "Incentivos Logtech", "Subsídio 4.0 PMEs"],
        "Impacto": ["Alto Valor Agregado", "Retenção de Talentos", "Aumento de Produtividade"]
    })
    st.table(acoes)

# --- 8. FONTES/REFERÊNCIAS ---
elif menu == "Fontes/Referências":
    st.markdown('<p class="section-title">Fontes de Dados</p>', unsafe_allow_html=True)
    st.write("- IBGE Cidades (PIB Municipal)")
    st.write("- Fundação SEADE (VAB Setorial)")
    st.write("- Novo CAGED (Empregos)")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <b>Observatório Industrial Votorantim | Ciência de Dados para Negócio</b><br>
        Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.<br>
        <i>Gerado em {datetime.now().strftime('%d/%m/%Y')}</i>
    </div>
    """, unsafe_allow_html=True)
