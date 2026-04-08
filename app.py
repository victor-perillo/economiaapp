import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analytics Industrial Votorantim | 4.0",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #1E3A8A; color: white; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SEÇÃO 1: ETL (Extraction, Transformation, Load) ---
@st.cache_data
def load_and_process_data():
    # 1. RAW DATA (Dados extraídos dos seus arquivos)
    # -----------------------------------------------
    
    # Dados de Segmentos e VAB
    segmentos_data = {
        'CNAE_Segmento': ["Minerais Não Metálicos (Cimento)", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'Participacao_VAB_Pct': [55, 20, 12, 8, 5],
        'Estoque_Emprego': [3100, 1950, 1100, 850, 600]
    }
    
    # Histórico de Produtividade e VAB
    pib_data = {
        'Ano': [2018, 2019, 2020, 2021],
        'VAB_Ind': [1520, 1610, 1740, 1920], # Milhões R$
        'VAB_Ser': [2100, 2250, 2380, 2750]
    }
    
    # Produtividade Calculada
    prod_data = {
        'Ano': [2019, 2020, 2021],
        'Produtividade': [190.5, 214.2, 223.2] # VAB/Emprego
    }

    # 2. TRANSFORMAÇÃO (Lógica de Ciência de Dados)
    # -----------------------------------------------
    df_seg = pd.DataFrame(segmentos_data)
    df_pib = pd.DataFrame(pib_data)
    df_prod = pd.DataFrame(prod_data)
    
    # Cálculo de crescimento anual do VAB Industrial
    df_pib['Crescimento_Ind'] = df_pib['VAB_Ind'].pct_change() * 100
    
    # Mapeamento para Indústria 4.0 (Baseado na complexidade do setor)
    # Setores de base (Cimento) têm alto potencial de automação, mas alta inércia
    mapa_40 = {
        "Minerais Não Metálicos (Cimento)": {"Maturidade": 0.65, "Gargalo": "Eficiência Energética"},
        "Metalurgia": {"Maturidade": 0.75, "Gargalo": "Integração de Cadeia"},
        "Química/Plásticos": {"Maturidade": 0.50, "Gargalo": "Digitalização"},
        "Alimentos": {"Maturidade": 0.40, "Gargalo": "Rastreabilidade"},
        "Outros": {"Maturidade": 0.30, "Gargalo": "Qualificação"}
    }
    df_seg['Maturidade_4.0'] = df_seg['CNAE_Segmento'].map(lambda x: mapa_40[x]['Maturidade'])
    df_seg['Gargalo_Principal'] = df_seg['CNAE_Segmento'].map(lambda x: mapa_40[x]['Gargalo'])
    
    return df_seg, df_pib, df_prod

df_seg, df_pib, df_prod = load_and_process_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b2/Bras%C3%A3o_de_Votorantim.PNG", width=80)
    st.title("Hub Industrial")
    st.markdown("---")
    aba = st.radio("Navegação Estratégica", 
                  ["📌 Panorama Econômico", "📊 Análise de Segmentos", "🤖 Indústria 4.0", "🚀 Plano de Ação"])
    st.markdown("---")
    st.info("**Fontes:** IBGE, SEADE e Dados Públicos de Votorantim.")

# --- TÍTULO PRINCIPAL ---
st.markdown(f"<h1>{aba}</h1>", unsafe_allow_html=True)

# --- ABA 1: PANORAMA ECONÔMICO ---
if aba == "📌 Panorama Econômico":
    st.markdown("""
    Votorantim possui uma história intrinsecamente ligada ao setor industrial. 
    Atualmente, o **Valor Adicionado Bruto (VAB)** da indústria representa um pilar fundamental da região administrativa de Sorocaba.
    """)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("VAB Industrial (2021)", "R$ 1,92 Bi", f"{df_pib['Crescimento_Ind'].iloc[-1]:.1f}%")
    with c2:
        st.metric("Produtividade Média", "R$ 223,2k", "↑ 4.2%")
    with c3:
        st.metric("Empregos Ativos", "8.920", "+2.1%")

    # Gráfico de Crescimento
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=df_pib['Ano'], y=df_pib['VAB_Ind'], name='VAB Indústria', line=dict(color='#1E3A8A', width=4)))
    fig_growth.add_trace(go.Scatter(x=df_pib['Ano'], y=df_pib['VAB_Ser'], name='VAB Serviços', line=dict(color='#10B981', dash='dash')))
    fig_growth.update_layout(title="Evolução do VAB (Indústria vs Serviços) - Votorantim", xaxis_title="Ano", yaxis_title="Milhões R$")
    st.plotly_chart(fig_growth, use_container_width=True)

# --- ABA 2: ANÁLISE DE SEGMENTOS ---
elif aba == "📊 Análise de Segmentos":
    st.markdown("### Identificação de Segmentos Baseada em CNAE")
    
    col_a, col_b = st.columns([0.6, 0.4])
    
    with col_a:
        fig_treemap = px.treemap(df_seg, path=['CNAE_Segmento'], values='Participacao_VAB_Pct',
                                 color='Estoque_Emprego', color_continuous_scale='Blues',
                                 title="Participação no Valor Adicionado por Segmento")
        st.plotly_chart(fig_treemap, use_container_width=True)
        
    with col_b:
        st.markdown("#### Distribuição de Mão de Obra")
        fig_bar = px.bar(df_seg.sort_values('Estoque_Emprego'), x='Estoque_Emprego', y='CNAE_Segmento', 
                         orientation='h', text_auto=True, color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig_bar, use_container_width=True)

    st.warning("⚠️ **Insight Econômico:** O setor de 'Minerais Não Metálicos' concentra 55% do VAB, indicando uma **alta dependência** do mercado de construção civil e do grupo Votorantim.")

# --- ABA 3: INDÚSTRIA 4.0 ---
elif aba == "🤖 Indústria 4.0":
    st.markdown("### Diagnóstico de Maturidade Digital")
    
    c4, c5 = st.columns(2)
    
    with c4:
        fig_polar = go.Figure()
        fig_polar.add_trace(go.Scatterpolar(
            r=df_seg['Maturidade_4.0'] * 100,
            theta=df_seg['CNAE_Segmento'],
            fill='toself',
            name='Nível de Digitalização',
            marker=dict(color='#1E3A8A')
        ))
        fig_polar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Score de Indústria 4.0 por Setor (%)")
        st.plotly_chart(fig_polar, use_container_width=True)
        
    with c5:
        st.markdown("#### 🚩 Identificação de Problemas")
        st.error("""
        1. **Baixa Interconectividade:** A maioria das indústrias têxteis e de alimentos ainda utiliza processos manuais de coleta de dados.
        2. **Gargalo Logístico:** Falta de rastreabilidade em tempo real nos CNAEs de minerais.
        3. **Gap de Talentos:** A produtividade cresceu 17% entre 2019-2021, mas o nível de automação inteligente não acompanhou na mesma proporção.
        """)
        
    st.info("💡 **Conceito Econômico:** A produtividade industrial de Votorantim (R$ 223k/habitante) é alta, mas corre risco de estagnação sem a implementação de **IoT (Internet das Coisas)** e **IA Preditiva**.")

# --- ABA 4: PLANO DE AÇÃO ---
elif aba == "🚀 Plano de Ação":
    st.subheader("Estratégia Transversal para Votorantim 2025-2030")
    
    # Plano de Ação em formato de colunas
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Modernização")
        st.write("""
        **Ação:** Implementação de Sensores IoT no setor de Cimento.
        **Objetivo:** Reduzir consumo de energia em 15%.
        **KPI:** Consumo de MWh / Tonelada produzida.
        """)
        
    with col2:
        st.markdown("### 2. Educação 4.0")
        st.write("""
        **Ação:** Parceria com SENAI/Fatec para cursos de Data Science Industrial.
        **Objetivo:** Requalificar 500 trabalhadores/ano.
        **KPI:** Taxa de retenção de talentos locais.
        """)
        
    with col3:
        st.markdown("### 3. Incentivos ESG")
        st.write("""
        **Ação:** Redução de IPTU para indústrias com certificação de 'Lixo Zero'.
        **Objetivo:** Atrair startups de economia circular.
        **KPI:** Número de novas empresas tech instaladas.
        """)

    st.markdown("---")
    st.subheader("Tabela de Priorização (Matriz de Impacto)")
    plano_df = pd.DataFrame({
        "Projeto": ["Smart Grid Industrial", "Digital Twins (Metalurgia)", "Hub de Dados Votorantim"],
        "Custo Est.": ["Alto", "Médio", "Baixo"],
        "Impacto PIB": ["Muito Alto", "Alto", "Médio"],
        "Prazo": ["36 meses", "18 meses", "12 meses"]
    })
    st.table(plano_df)

    st.success("📝 **Conclusão:** O futuro econômico de Votorantim depende da transição da força bruta (extração) para a força analítica (dados).")
