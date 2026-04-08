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
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1E3A8A; }
    .section-title { color: #1E3A8A; font-weight: bold; border-left: 8px solid #FF8C00; padding-left: 15px; margin-top: 30px; margin-bottom: 20px; font-size: 26px; }
    .chart-caption { background-color: #e9ecef; padding: 15px; border-radius: 0 0 10px 10px; border-top: 3px solid #1E3A8A; font-size: 14px; color: #333; font-style: italic; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; border-top: 1px solid #ddd; }
    .highlight { color: #1E3A8A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS (BASEADO NO PDF) ---
@st.cache_data
def load_data():
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], 
        'Ganho_Eficiencia': [15, 22, 18, 10, 12],
        'Maturidade_Atual': [2.4, 3.1, 2.8, 1.9, 2.5] 
    })
    
    # Dados extraídos das páginas 5 e 7 do PDF
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'Produtividade': [175, 190, 214, 223, 238, 255], 
        'VAB_Indústria': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Serviços': [2100, 2250, 2380, 2750, 3100, 3500]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=80)
    st.title("Hub de Inteligência")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Selecione o Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Introdução & Contexto", "Metodologia (ETL)", "Dashboard Executivo", 
                    "Análise de Maturidade 4.0", "Projeção Futura", "Plano de Ação"])

# Lógica de Filtragem Corrigida
if ano_selecionado == "Todos":
    df_filtered = df_hist
    # Para o KPI em "Todos", pegamos o dado mais recente em vez de somar
    display_df = df_hist.iloc[[-1]] 
else:
    df_filtered = df_hist[df_hist['Ano'] == int(ano_selecionado)]
    display_df = df_filtered

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Cenário e Contexto Econômico</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        Votorantim/SP possui um legado industrial robusto focado em indústria de base[cite: 7]. 
        O dataset mostra uma transição: a indústria perde share para o setor de Serviços, indicando modernização da matriz[cite: 8].
        <br><br>
        <span class="highlight">O Efeito Shadowing:</span> A proximidade com Sorocaba gera uma sombra econômica; Sorocaba atrai o alto valor agregado enquanto Votorantim retém a indústria de base[cite: 9, 10].
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Problemas Identificados</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Risco de Setor Único:** Dependência de poucos players gigantes (Grupo Votorantim)[cite: 81, 111].")
        st.warning("**Conflito de Zoneamento:** Trade-off entre expansão imobiliária e manutenção fabril[cite: 87, 88].")
    with c2:
        st.error("**Skill Gap:** Desalinhamento entre o perfil local e as demandas da Indústria 4.0[cite: 84, 85].")
        st.info("**Baixo Valor Agregado:** Setores com alto impacto ambiental e baixa geração de dados[cite: 10, 12].")

# --- 2. METODOLOGIA (ETL) ---
elif menu == "Metodologia (ETL)":
    st.markdown('<p class="section-title">Processamento de Dados (ETL)</p>', unsafe_allow_html=True)
    st.write("**Extração:** Dados de IBGE, SEADE e Novo CAGED[cite: 15].")
    st.write("**Transformação:** Limpeza de nulos, padronização CNAE e Join por Código de Município[cite: 18, 19, 20].")
    st.write("**Carga:** Estruturação em DataFrames Pandas para consumo imediato[cite: 22].")

# --- 3. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macroeconômico</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("VAB Indústria", f"R$ {display_df['VAB_Indústria'].values[0]}M")
    with c2:
        st.metric("VAB Serviços", f"R$ {display_df['VAB_Serviços'].values[0]}M")
    with c3:
        st.metric("Produtividade Média", f"{display_df['Produtividade'].values[0]}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_filtered, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'],
                              title="Evolução Setorial",
                              color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"}, markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">O setor de Serviços acelera mais rápido que a Indústria, sinalizando a "terceirização" da cidade[cite: 68, 69].</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.5, title="Riqueza por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)
        st.markdown('<div class="chart-caption">Minerais Não Metálicos detêm 55% da riqueza industrial[cite: 107].</div>', unsafe_allow_html=True)

# --- 4. INDÚSTRIA 4.0 ---
elif menu == "Análise de Maturidade 4.0":
    st.markdown('<p class="section-title">Diagnóstico Digital</p>', unsafe_allow_html=True)
    st.write("A produtividade cresce acima da contratação, provando o uso de tecnologia e automação[cite: 110, 138].")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_filtered, x='Ano', y='Produtividade', title="Produtividade (R$ / Trabalhador)", color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#1E3A8A')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Índice de Maturidade")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 5. PROJEÇÃO FUTURA (NOVA SEÇÃO) ---
elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Tendência Econômica (Próximos 5 e 10 Anos)</p>', unsafe_allow_html=True)
    
    # Modelo Simples de Regressão Linear para Projeção
    anos_hist = df_hist['Ano'].values
    anos_proj = np.array([2024, 2025, 2026, 2027, 2028, 2033])
    
    def projetar(valores):
        coef = np.polyfit(anos_hist, valores, 1)
        return np.polyval(coef, anos_proj)

    proj_ind = projetar(df_hist['VAB_Indústria'].values)
    proj_serv = projetar(df_hist['VAB_Serviços'].values)

    df_proj = pd.DataFrame({
        'Ano': anos_proj,
        'VAB_Indústria': proj_ind,
        'VAB_Serviços': proj_serv,
        'Tipo': 'Projeção'
    })
    
    df_completo = pd.concat([df_hist.assign(Tipo='Histórico'), df_proj])

    fig_proj = px.line(df_completo, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'], color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"},
                      line_dash='Tipo', title="Projeção de Cenário: Manutenção do Desempenho Atual")
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.markdown(f"""
    <div class="card">
        <b>Análise de Tendência:</b> Se o desempenho atual for mantido, em 10 anos (2033), o setor de <b>Serviços</b> atingirá aproximadamente 
        R$ {proj_serv[-1]:.0f}M, enquanto a <b>Indústria</b> chegará a R$ {proj_ind[-1]:.0f}M. 
        O gap entre os setores continuará se alargando, reforçando a necessidade de ações do Plano Estratégico para valorizar a base industrial.
    </div>
    """, unsafe_allow_html=True)

# --- 6. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano de Ação Estratégico</p>', unsafe_allow_html=True)
    st.write("Ações para mitigar a dependência econômica e o gap de mão de obra[cite: 141, 155].")
    
    st.table(pd.DataFrame({
        "Eixo": ["1. Diversificação Vertical", "2. Hub de Dados", "3. Green Tech", "4. Simbiose Industrial", "5. Requalificação 4.0"],
        "Ação": ["Atrair manufatura leve que use insumo local", "Centro de treinamento em IA/IoT", "Subsídios para energia limpa", "Reuso de resíduos entre indústrias", "Atualização do currículo técnico"]
    }))

# --- FOOTER ---
st.markdown(f"""<div class="footer"><p>Observatório Industrial Votorantim | Gerado em {datetime.now().strftime('%d/%m/%Y')}</p></div>""", unsafe_allow_html=True)
