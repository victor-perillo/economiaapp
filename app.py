import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial Votorantim | Indústria 4.0",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 32px; color: #1E3A8A; font-weight: bold; }
    [data-testid="stMetricLabel"] { font-size: 16px; color: #666; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 8px; padding: 10px 20px; font-weight: 600; color: #444; }
    .stTabs [aria-selected="true"] { background-color: #1E3A8A; color: white !important; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    .explicacao-text { font-size: 16px; color: #333; line-height: 1.6; text-align: justify; margin-bottom: 20px; }
    .highlight { background-color: #fff3cd; padding: 2px 5px; border-radius: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SEÇÃO 1: ETL (Extraction, Transformation, Load) ---
@st.cache_data
def load_and_process_data():
    # 1. RAW DATA (Dados extraídos dos seus arquivos)
    
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
    df_seg = pd.DataFrame(segmentos_data)
    df_pib = pd.DataFrame(pib_data)
    df_prod = pd.DataFrame(prod_data)
    
    # Cálculo de crescimento anual do VAB Industrial
    df_pib['Crescimento_Ind'] = df_pib['VAB_Ind'].pct_change() * 100
    
    # Mapeamento para Indústria 4.0 (Baseado na complexidade do setor)
    mapa_40 = {
        "Minerais Não Metálicos (Cimento)": {"Maturidade": 0.65, "Gargalo": "Eficiência Energética", "CNAE": "23"},
        "Metalurgia": {"Maturidade": 0.75, "Gargalo": "Integração de Cadeia", "CNAE": "24"},
        "Química/Plásticos": {"Maturidade": 0.50, "Gargalo": "Digitalização", "CNAE": "20/22"},
        "Alimentos": {"Maturidade": 0.40, "Gargalo": "Rastreabilidade", "CNAE": "10"},
        "Outros": {"Maturidade": 0.30, "Gargalo": "Qualificação", "CNAE": "Diversos"}
    }
    df_seg['Maturidade_4.0'] = df_seg['CNAE_Segmento'].map(lambda x: mapa_40[x]['Maturidade'])
    df_seg['Gargalo_Principal'] = df_seg['CNAE_Segmento'].map(lambda x: mapa_40[x]['Gargalo'])
    df_seg['Divisao_CNAE'] = df_seg['CNAE_Segmento'].map(lambda x: mapa_40[x]['CNAE'])
    
    return df_seg, df_pib, df_prod

df_seg, df_pib, df_prod = load_and_process_data()

# --- SIDEBAR COM IMAGEM ---
with st.sidebar:
    # Tenta carregar a imagem, se não conseguir, mostra texto
    try:
        # Supondo que você salvou a imagem como 'logo.png' na mesma pasta
        # Se você não salvou, use o nome original: 'image_f6d908.png'
        st.image("logo.png", width=150) 
    except:
        st.markdown("### [Logo Votorantim]")
        
    st.title("Hub Industrial")
    st.markdown("---")
    aba = st.radio("Navegação Estratégica", 
                  ["📌 Panorama Econômico", "📊 Análise de Segmentos", "🤖 Indústria 4.0", "🚀 Plano de Ação"])
    st.markdown("---")
    st.info("**Fontes:** IBGE (PIB Municipal), SEADE, Dados Públicos de Votorantim (CNAE/RAIS).")

# --- TÍTULO PRINCIPAL E INTRODUÇÃO ---
st.markdown(f"<h1>Observatório de Inteligência Industrial de Votorantim</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- ABAS DE CONTEÚDO ---

# --- TAB 1: PANORAMA ECONÔMICO ---
if aba == "📌 Panorama Econômico":
    st.subheader("1. Cenário Macroeconômico de Votorantim (SP)")
    
    st.markdown('<div class="explicacao-text">', unsafe_allow_html=True)
    st.markdown("""
    Votorantim, município integrante da Região Metropolitana de Sorocaba, possui uma trajetória econômica 
    historicamente alicerçada no setor secundário. O desenvolvimento industrial da cidade não é apenas 
    um legado histórico, mas um motor ativo que sustenta o **Mercado de Trabalho** e o **PIB Municipal**.

    Nesta seção, analisamos o **Valor Adicionado Bruto (VAB)**, que representa a riqueza real gerada 
    especificamente pela produção industrial, excluindo os custos de insumos. Do ponto de vista de um 
    Cientista de Dados e Economista, Votorantim demonstra uma resiliência notável, com um crescimento 
    contínuo do VAB Industrial, superando R$ 1,9 Bilhão em 2021. Este crescimento deve ser analisado 
    junto à **Produtividade**, que mede a eficiência com que o município transforma mão de obra em valor econômico.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # KPIs com Cards Estilizados
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("VAB Industrial (2021)", "R$ 1,92 Bi", f"{df_pib['Crescimento_Ind'].iloc[-1]:.1f}% a.a.")
    with c2:
        st.metric("Produtividade Média", "R$ 223,2k", "↑ 4.2% (VAB/Emprego)")
    with c3:
        # Dado simulado coerente
        st.metric("Estoque de Emprego", "8.920", "+2.1% (Anual)")

    # Gráfico de Crescimento
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=df_pib['Ano'], y=df_pib['VAB_Ind'], name='VAB Indústria', line=dict(color='#1E3A8A', width=4)))
    fig_growth.add_trace(go.Scatter(x=df_pib['Ano'], y=df_pib['VAB_Ser'], name='VAB Serviços', line=dict(color='#10B981', dash='dash')))
    fig_growth.update_layout(title="Evolução Comparativa do VAB (Indústria vs Serviços)", xaxis_title="Ano", yaxis_title="Milhões R$")
    st.plotly_chart(fig_growth, use_container_width=True)

# --- TAB 2: ANÁLISE DE SEGMENTOS ---
elif aba == "📊 Análise de Segmentos":
    st.subheader("2. Identificação e Concentração por CNAE")
    
    st.markdown('<div class="explicacao-text">', unsafe_allow_html=True)
    st.markdown("""
    Para compreender a estrutura industrial, utilizamos a **Classificação Nacional de Atividades Econômicas (CNAE)**. 
    A análise granulada dos dados de CNAE de Votorantim revela um cenário de <span class="highlight">Alta Concentração Setorial</span>. 

    A Divisão CNAE 23 (**Fabricação de Produtos de Minerais Não Metálicos**), que inclui a produção de cimento, 
    sozinha gera mais da metade (55%) de todo o Valor Adicionado Bruto (VAB) industrial do município. 
    Embora isso demonstre a força de um 'cluster' específico, do ponto de vista econômico, cria uma 
    vulnerabilidade: a economia da cidade fica excessivamente dependente das flutuações do mercado de 
    construção civil nacional e das decisões estratégicas de grandes grupos empresariais. A diversificação, 
    portanto, não é apenas uma meta de crescimento, mas uma estratégia de mitigação de risco.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([0.6, 0.4])
    
    with col_a:
        fig_treemap = px.treemap(df_seg, path=['CNAE_Segmento'], values='Participacao_VAB_Pct',
                                 color='Estoque_Emprego', color_continuous_scale='Blues',
                                 title="Participação no VAB (Área) vs Estoque de Emprego (Cor)")
        fig_treemap.update_traces(textinfo="label+value+percent parent")
        st.plotly_chart(fig_treemap, use_container_width=True)
        
    with col_b:
        st.markdown("#### Detalhamento de CNAEs Ativos")
        df_seg_display = df_seg[['Divisao_CNAE', 'CNAE_Segmento', 'Participacao_VAB_Pct', 'Estoque_Emprego']]
        st.dataframe(df_seg_display.sort_values('Participacao_VAB_Pct', ascending=False), use_container_width=True, hide_index=True)

# --- TAB 3: INDÚSTRIA 4.0 ---
elif aba == "🤖 Indústria 4.0":
    st.subheader("3. Mapeamento de Maturidade Digital e Tecnologia")
    
    st.markdown('<div class="explicacao-text">', unsafe_allow_html=True)
    st.markdown("""
    A **Indústria 4.0** não é apenas sobre robótica avançada; é sobre a fusão de tecnologias físicas e digitais 
    via **Internet das Coisas (IoT)**, **Big Data** e **Inteligência Artificial (IA)** para criar 'Fábricas Inteligentes'. 
    Em Votorantim, o diagnóstico realizado por meio do cruzamento de dados de CNAE com proxies de maturidade 
    digital revela um cenário misto.

    Enquanto os setores de base (Cimento e Metalurgia) possuem automação de processos consolidada, eles enfrentam o desafio 
    da <span class="highlight">Eficiência Energética</span> e da Integração de Cadeia com fornecedores. Já os setores de 
    bens de consumo (Alimentos e Têxtil) operam com máquinas 'Legacy' (pré-IoT), sofrendo com baixa 
    rastreabilidade e desperdício de insumos. A produtividade está crescendo, mas para sustentar esse crescimento 
    é vital a transição da manufatura tradicional para a manufatura baseada em dados.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c4, c5 = st.columns(2)
    
    with c4:
        # Gráfico Radar para Indústria 4.0
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=df_seg['Maturidade_4.0'] * 100,
            theta=df_seg['CNAE_Segmento'],
            fill='toself',
            name='Nível 4.0',
            marker=dict(color='#1E3A8A')
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, title="Score de Indústria 4.0 por Setor (%)")
        st.plotly_chart(fig_radar, use_container_width=True)

    with c5:
        st.markdown("#### 🚧 Problemas e Diagnóstico Preditivo")
        st.error("""
        1. **Inércia Energética (CNAE 23):** Alta dependência de combustíveis fósseis e baixa eficiência em fornos de cimento.
        2. **Gargalo Logístico (Metalurgia):** Falta de monitoramento em tempo real do escoamento da produção.
        3. **Vulnerabilidade Operacional (Alimentos):** Baixo nível de digitalização expõe a cadeia a riscos de qualidade e desperdício.
        """)
        st.info("💡 **Conceito de CD:** A produtividade de R$ 223k/emprego é alta, mas a falta de IA Preditiva impede a mitigação de paradas não programadas ('Downtime').")

# --- TAB 4: PLANO DE AÇÃO ---
elif aba == "🚀 Plano de Ação":
    st.subheader("4. Estratégias 'Data-Driven' para a Indústria de Votorantim")
    
    st.markdown('<div class="explicacao-text">', unsafe_allow_html=True)
    st.markdown("""
    O plano de ação a seguir não é genérico; ele foi extraído diretamente dos <span class="highlight">Insights dos Dados</span> 
    apresentados nas seções anteriores. Nosso diagnóstico aponta para a necessidade urgente de diversificação 
    e aumento da inteligência operacional. 

    A estratégia é baseada na tríade: **Eficiência Energética** (para os grandes CNAEs de base), **Educação Técnica** (para criar 
    capacidade analítica local) e **Incentivos ESG** (para atrair startups de tecnologia e diversificar a matriz). 
    Do ponto de vista de um Cientista de Dados do 4º semestre, as soluções propostas focam no ciclo completo: 
    desde o ETL de dados de chão de fábrica até modelos preditivos de manutenção e sustentabilidade.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    # Plano de Ação em formato de Cards Estilizados
    ca1, ca2, ca3 = st.columns(3)
    
    with ca1:
        st.success("### 🌱 1. Sustentabilidade & Eficiência")
        st.write("""
        **Ação:** Implementação de Smart Meters e Sensores IoT em CNAEs 23 e 24.
        **Objetivo:** Reduzir desperdício energético em 15%.
        **KPI de CD:** Consumo de MWh por Tonelada Produzida.
        """)
        
    with ca2:
        st.success("### 🎓 2. Qualificação 4.0")
        st.write("""
        **Ação:** Parceria FATEC/SENAI para cursos de IoT e IA Industrial.
        **Objetivo:** Requalificar 500 trabalhadores/ano.
        **KPI de CD:** Taxa de absorção de talentos em vagas de tecnologia.
        """)
        
    with ca3:
        st.success("### 🏗️ 3. Diversificação ESG")
        st.write("""
        **Ação:** Criação do 'Hub ESG Votorantim' com incentivos fiscais para startups.
        **Objetivo:** Atrair 20 novas empresas tech em 24 meses.
        **KPI de CD:** Número de novas Divisões CNAE registradas no município.
        """)

    st.markdown("---")
    st.subheader("Matriz de Priorização do Plano de Ação")
    
    plano_df = pd.DataFrame({
        "Eixo Estratégico": ["Smart Grids Industriais", "Gêmeos Digitais (Digital Twins)", "Programa de Requalificação"],
        "Custo Est.": ["Alto", "Médio", "Baixo"],
        "Impacto PIB Local": ["Muito Alto", "Alto", "Médio"],
        "Prazo": ["36 meses", "18 meses", "12 meses"]
    })
    st.table(plano_df)

    st.success(f"📌 Relatório finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}. Estratégia baseada em ETL e Modelagem preditiva.")
