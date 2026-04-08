import streamlit as st
import pandas as pd
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

# --- CARREGAMENTO E CORREÇÃO DE DADOS ---
@st.cache_data
def load_data():
    # Participação Industrial por CNAE
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], 
        'Ganho_Eficiencia': [15, 22, 18, 10, 12],
        'Maturidade_Atual': [2.4, 3.1, 2.8, 1.9, 2.5] 
    })
    
    # Histórico de VAB Corrigido (Valores em R$ Milhões)
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'Produtividade': [175, 190, 214, 223, 238, 255], 
        'VAB_Indústria': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Serviços': [2100, 2250, 2380, 2750, 3100, 3500]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR COM FILTRO TEMPORAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=80)
    st.title("Hub de Inteligência")
    
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Selecione o Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Introdução & Contexto", "Metodologia (ETL)", "Dashboard Executivo", "Análise de Maturidade 4.0", "Plano de Ação"])

# Filtragem Dinâmica
if ano_selecionado == "Todos":
    df_filtered = df_hist
else:
    df_filtered = df_hist[df_hist['Ano'] == int(ano_selecionado)]

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Cenário e Contexto Econômico</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        Votorantim/SP possui um legado industrial robusto focado em indústria de base. 
        Contudo, os dados mostram que a indústria está perdendo participação relativa no PIB para o setor de Serviços.
        <br><br>
        <span class="highlight">O Efeito Shadowing:</span> A proximidade com Sorocaba gera uma sombra econômica. 
        Enquanto a vizinha atrai setores tecnológicos, Votorantim mantém indústrias de base com maior impacto ambiental.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Problemas Identificados</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Risco de Setor Único:** Dependência excessiva de poucos players gigantes.")
        st.warning("**Conflito de Zoneamento:** Expansão urbana avançando sobre áreas industriais.")
    with c2:
        st.error("**Skill Gap:** Mão de obra local ainda desalinhada com a automação digital.")
        st.info("**Dependência de Base:** Necessidade de diversificar para indústrias de dados.")

# --- 2. METODOLOGIA (ETL) ---
elif menu == "Metodologia (ETL)":
    st.markdown('<p class="section-title">Processamento de Dados (ETL)</p>', unsafe_allow_html=True)
    
    col_etl1, col_etl2 = st.columns(2)
    with col_etl1:
        st.markdown("### 📥 Extração & Transformação")
        st.write("1. **Fontes:** IBGE Cidades, SEADE e Novo CAGED.")
        st.write("2. **Limpeza:** Remoção de registros nulos e tratamento de lag temporal.")
        st.write("3. **Padronização:** Unificação de CNAEs para Minerais Não Metálicos.")
    
    with col_etl2:
        st.markdown("### 🔄 Unificação & Carga")
        st.write("4. **Join:** Merge de bases via Código de Município e Ano.")
        st.write("5. **Carga:** Estruturação em DataFrames Pandas para consumo no Streamlit.")

# --- 3. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macroeconômico</p>', unsafe_allow_html=True)
    
    # KPIs dinâmicos baseados no filtro
    c1, c2, c3 = st.columns(3)
    with c1:
        vab_ind = df_filtered['VAB_Indústria'].sum()
        st.metric("VAB Indústria", f"R$ {vab_ind}M")
    with c2:
        vab_serv = df_filtered['VAB_Serviços'].sum()
        st.metric("VAB Serviços", f"R$ {vab_serv}M")
    with c3:
        prod_med = df_filtered['Produtividade'].mean()
        st.metric("Produtividade Média", f"{prod_med:.1f}k")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_filtered, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'],
                              title="Crescimento Setorial: Indústria vs Serviços",
                              color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"}, 
                              markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Resumo:</b> O gráfico demonstra a aceleração do setor de serviços em relação à indústria, confirmando a transição da matriz econômica municipal.</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.5, title="Riqueza por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Nota:</b> O segmento de Cimento domina 55% da produção industrial local.</div>', unsafe_allow_html=True)

# --- 4. INDÚSTRIA 4.0 ---
elif menu == "Análise de Maturidade 4.0":
    st.markdown('<p class="section-title">Diagnóstico Digital</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_filtered, x='Ano', y='Produtividade', title="Produtividade (R$ / Trabalhador)", color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Evidência:</b> O aumento da produtividade indica investimentos em automação e sensoriamento IoT.</div>', unsafe_allow_html=True)

    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', name='Maturidade', marker=dict(color='#1E3A8A')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Índice de Maturidade Digital")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 5. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Plano de Ação Estratégico</p>', unsafe_allow_html=True)
    
    st.table(pd.DataFrame({
        "Eixo Estratégico": [
            "1. Diversificação Vertical", 
            "2. Hub de Dados Regional", 
            "3. Green Tech Incentives",
            "4. Simbiose Industrial",
            "5. Requalificação 4.0"
        ],
        "Descrição": [
            "Atrair manufatura leve que utilize o insumo de cimento local.",
            "Centro de treinamento em IA e IoT em parceria regional.",
            "Subsídios fiscais para energia limpa e créditos de carbono.",
            "Integração de clusters para reaproveitamento de resíduos industriais.",
            "Atualização curricular focada em análise de dados industriais."
        ]
    }))

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Observatório Industrial Votorantim</b> | Fatec Votorantim</p>
        <p>Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p>Atualizado em: {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)
