import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configurações Iniciais
st.set_page_config(page_title="Análise Industrial Votorantim", layout="wide", page_icon="🏭")

# Estilização básica via Markdown
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar (Navegação e Filtros)
st.sidebar.image("https://www.votorantim.sp.gov.br/img/logo.png", width=200) # Exemplo de logo
st.sidebar.title("Navegação")
aba_selecionada = st.sidebar.radio("Ir para:", ["Dashboard Geral", "Análise de CNAEs", "Diagnóstico e Ações"])

st.sidebar.markdown("---")
st.sidebar.info("Projeto: Análise das Indústrias de Votorantim\n\nAcadêmico: 4º Semestre CD")

# 3. Carregamento de Dados (Simulação)
@st.cache_data
def carregar_dados():
    # Substitua esta parte pelo carregamento do seu CSV ou Excel
    data = {
        'CNAE': ['23.30-3', '24.21-0', '13.21-9', '23.92-3', '10.91-1'],
        'Segmento': ['Cimento/Concreto', 'Metalurgia', 'Têxtil', 'Minerais não-metálicos', 'Alimentos'],
        'Quantidade': [45, 32, 28, 15, 40],
        'Empregos': [2500, 1800, 1200, 900, 600],
        'PIB_Contribuicao': [35, 20, 15, 10, 20]
    }
    return pd.DataFrame(data)

df = carregar_dados()

# --- ABA 1: DASHBOARD GERAL ---
if aba_selecionada == "Dashboard Geral":
    st.title("🏭 Panorama Industrial de Votorantim")
    st.write("Análise macroeconômica baseada em dados públicos (IBGE/Cade).")
    
    # KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Indústrias", df['Quantidade'].sum(), "+2% vs 2024")
    m2.metric("Segmento Líder", df.iloc[0]['Segmento'])
    m3.metric("Mão de Obra Industrial", f"{df['Empregos'].sum()} postos")

    # Gráficos Principais
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Distribuição por Segmento")
        fig_pizza = px.pie(df, values='Quantidade', names='Segmento', hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pizza, use_container_width=True)
        
    with c2:
        st.subheader("Impacto Econômico por Setor (%)")
        fig_bar = px.bar(df.sort_values('PIB_Contribuicao'), x='PIB_Contribuicao', y='Segmento', 
                         orientation='h', text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)

# --- ABA 2: ANÁLISE DE CNAEs ---
elif aba_selecionada == "Análise de CNAEs":
    st.title("🔍 Detalhamento por CNAE")
    
    st.markdown("""
    A classificação por **CNAE (Classificação Nacional de Atividades Econômicas)** permite identificar 
    especificamente onde a força produtiva de Votorantim está concentrada.
    """)
    
    # Treemap para visualização hierárquica
    fig_tree = px.treemap(df, path=['Segmento', 'CNAE'], values='Empregos',
                         title="Volume de Empregos por Hierarquia Industrial")
    st.plotly_chart(fig_tree, use_container_width=True)
    
    st.dataframe(df.style.highlight_max(axis=0, subset=['Empregos'], color='#d4edda'), use_container_width=True)

# --- ABA 3: DIAGNÓSTICO E AÇÕES ---
elif aba_selecionada == "Diagnóstico e Ações":
    st.title("🧠 Insights e Plano de Estratégico")

    # Colunas de análise SWOT ou Problema/Solução
    col_p, col_s = st.columns(2)
    
    with col_p:
        st.error("### 🚩 Identificação de Problemas")
        st.markdown("""
        1. **Concentração Setorial:** Alta dependência do setor de minerais e cimento (CNAE 23.30-3).
        2. **Gargalo Logístico:** Identificado aumento no custo de escoamento em setores de base.
        3. **Vulnerabilidade:** Baixa digitalização nas indústrias têxteis locais.
        """)
        
    with col_s:
        st.success("### 💡 Insights Baseados em Dados")
        st.markdown("""
        - O setor de **Alimentos** apresenta o maior potencial de crescimento em número de unidades.
        - Existe uma correlação positiva entre o CNAE de Metalurgia e a geração de empregos qualificados.
        - **Oportunidade:** Reaproveitamento de resíduos industriais para Economia Circular.
        """)

    st.markdown("---")
    st.subheader("📋 Plano de Ação Sugerido")
    
    acoes = {
        "Ação": ["Programa 'Votorantim Digital'", "Incentivo à Economia Circular", "Diversificação de Matriz"],
        "Público Alvo": ["Pequenas Indústrias", "Setor de Minerais/Cimento", "Novos Investidores"],
        "Impacto": ["Alto", "Médio", "Muito Alto"],
        "Prazo": ["12 meses", "24 meses", "36 meses"]
    }
    st.table(pd.DataFrame(acoes))
    
    # Espaço para texto econômico
    st.info("""
    **Conclusão Econômica:** Do ponto de vista de um cientista de dados, Votorantim possui uma estrutura industrial robusta 
    mas rígida. A diversificação para setores de tecnologia e valor agregado (Indústria 4.0) é essencial para 
    mitigar riscos de flutuação em commodities de construção civil.
    """)
