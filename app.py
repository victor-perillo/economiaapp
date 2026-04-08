import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #1E3A8A; color: white; text-align: center; padding: 10px; font-size: 14px; z-index: 100; }
    .highlight { background-color: #fff3cd; padding: 2px 5px; border-radius: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SEÇÃO 1: ETL (Processamento de Dados baseado no PDF) ---
@st.cache_data
def load_and_process_data():
    # 1. EXTRAÇÃO (Fontes mencionadas no PDF)
    # Fontes: IBGE Cidades, SEADE e Novo CAGED
    
    segmentos_data = {
        'CNAE_Segmento': ["Minerais Não Metálicos (Cimento)", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'Participacao_VAB_Pct': [55, 20, 12, 8, 5],
        'Estoque_Emprego': [3100, 1950, 1100, 850, 600]
    }
    
    # Histórico de VAB (Baseado no Gráfico 1 do PDF)
    pib_data = {
        'Ano': [2018, 2019, 2020, 2021],
        'Indústria': [1520, 1610, 1740, 1920], 
        'Serviços': [2100, 2250, 2380, 2750]
    }
    
    # Dados de Planejamento (Cenário Atual vs Meta - Página 9 do PDF)
    meta_data = {
        'Setor': ["Cimento", "Metalurgia", "Novas Techs", "Outros"],
        'Atual': [55, 20, 5, 20],
        'Meta': [40, 20, 25, 15]
    }

    # 2. TRANSFORMAÇÃO
    df_seg = pd.DataFrame(segmentos_data)
    df_pib = pd.DataFrame(pib_data)
    df_meta = pd.DataFrame(meta_data)
    
    # Padronização e Unificação (Join simulado)
    df_pib['Crescimento_Ind'] = df_pib['Indústria'].pct_change() * 100
    
    return df_seg, df_pib, df_meta

df_seg, df_pib, df_meta = load_and_process_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Hub Industrial")
    st.markdown("---")
    aba = st.radio("Navegação Estratégica", 
                  ["📌 Panorama & Metodologia", "📊 Análise de Segmentos", "🤖 Diagnóstico 4.0", "🚀 Planejamento"])
    
    st.markdown("---")
    st.markdown("### Fontes de Dados")
    st.caption("• **IBGE:** Séries de PIB")
    st.caption("• **SEADE:** VAB Setorial")
    st.caption("• **CAGED:** Empregos Formais")

# --- CONTEÚDO PRINCIPAL ---
st.title("Observatório de Inteligência Industrial de Votorantim")

# --- TAB 1: PANORAMA & METODOLOGIA (LIGANDO OS PONTOS) ---
if aba == "📌 Panorama & Metodologia":
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.subheader("O Fenômeno do Shadowing e Transição")
        st.markdown(f"""
        Votorantim vive um momento crítico de sua história econômica. Enquanto carrega um forte **legacy industrial** focado em indústrias de base, os dados mostram um efeito de **'Shadowing' de Sorocaba**. 
        
        * **O Desafio:** Votorantim retém setores de baixo valor agregado e alto impacto ambiental, enquanto a vizinha atrai Tech e Automotiva.
        * **A Transição:** O setor de Serviços cresce em ritmo acelerado, indicando uma mudança de matriz econômica.
        """)
        
        # Gráfico Comparativo Indústria vs Serviços
        fig_pib = px.line(df_pib, x='Ano', y=['Indústria', 'Serviços'], markers=True,
                         title="Evolução do VAB: Aceleração do Setor de Serviços (R$ Milhões)",
                         color_discrete_map={"Indústria": "#1E3A8A", "Serviços": "#FF8C00"})
        st.plotly_chart(fig_pib, use_container_width=True)

    with col2:
        st.subheader("⚙️ Processo ETL")
        with st.expander("Ver etapas de Extração e Transformação", expanded=True):
            st.info("""
            **1. Extração:**
            Coleta de dados brutos (CSV/JSON) via APIs do SIDRA/IBGE e Novo CAGED.
            
            **2. Transformação:**
            * **Limpeza:** Remoção de nulos (PIB Municipal possui lag de 2 anos).
            * **Padronização:** Unificação de CNAEs (Ex: Fabricação de Cimento agrupada em 'Minerais não Metálicos').
            * **Join:** Merge de bases de Emprego e PIB usando Código IBGE.
            
            **3. Carga:**
            Dataset estruturado em DataFrames e exportado para consumo visual.
            """)

# --- TAB 2: ANÁLISE DE SEGMENTOS ---
elif aba == "📊 Análise de Segmentos":
    st.subheader("Análise de Concentração e Risco Setorial")
    
    c1, c2 = st.columns([0.4, 0.6])
    
    with c1:
        st.warning("### Risco de Setor Único")
        st.markdown("""
        O setor de **Cimento e Minerais** detém mais de **55% da riqueza industrial** da cidade. 
        Isso cria uma dependência sistêmica: se a construção civil sofre um choque, o impacto no município é total.
        """)
        
        fig_donut = px.pie(df_seg, values='Participacao_VAB_Pct', names='CNAE_Segmento', hole=.4,
                          title="Concentração de VAB por CNAE", color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        st.markdown("#### Distribuição de Força de Trabalho vs. Riqueza")
        fig_bar = px.bar(df_seg, x='CNAE_Segmento', y='Estoque_Emprego', 
                         color='Participacao_VAB_Pct',
                         labels={'Estoque_Emprego': 'Postos de Trabalho', 'Participacao_VAB_Pct': '% do VAB'},
                         title="Empregos por Setor (Cor indica contribuição no PIB)")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 3: DIAGNÓSTICO 4.0 ---
elif aba == "🤖 Diagnóstico 4.0":
    st.subheader("Resiliência e Skill Gap")
    
    col_prod, col_gap = st.columns(2)
    
    with col_prod:
        st.markdown("#### Produtividade (VAB por Trabalhador)")
        # Simulação de produtividade crescente conforme PDF
        st.success("📈 **Evidência:** A saída financeira cresce acima da contratação, indicando adoção de tecnologia.")
        prod_fig = px.bar(x=[2019, 2020, 2021], y=[190, 214, 223], 
                         title="Produtividade: Valor Gerado por Trabalhador (R$ Mil)",
                         labels={'x': 'Ano', 'y': 'R$ Mil/Trabalhador'}, color_discrete_sequence=['#008080'])
        st.plotly_chart(prod_fig, use_container_width=True)

    with col_gap:
        st.error("#### Problemas Identificados")
        st.markdown("""
        * **Skill Gap:** Desalinhamento entre o perfil analógico do trabalhador e as demandas da Indústria 4.0 (IA e IoT).
        * **Conflito de Zoneamento:** Setor imobiliário avançando sobre áreas industriais, limitando a expansão.
        * **Downtime:** Setores de base ainda sofrem com paradas que poderiam ser evitadas com sensoriamento preditivo.
        """)

# --- TAB 4: PLANEJAMENTO ---
elif aba == "🚀 Planejamento":
    st.subheader("Estratégia de Diversificação Industrial")
    
    st.markdown("""
    Para reduzir o risco de concentração, o planejamento estratégico foca em atrair **Indústrias de Manufatura Leve** e criar um 
    **Hub de Dados Regional**.
    """)
    
    # Gráfico de Metas (Cenário Atual vs Plano de Ação)
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(name='Cenário Atual', x=df_meta['Setor'], y=df_meta['Atual'], marker_color='#1E3A8A'))
    fig_meta.add_trace(go.Bar(name='Meta (Plano de Ação)', x=df_meta['Setor'], y=df_meta['Meta'], marker_color='#FF8C00'))
    
    fig_meta.update_layout(barmode='group', title="Diversificação de Portfólio Industrial: Hoje vs Futuro (%)")
    st.plotly_chart(fig_meta, use_container_width=True)
    
    st.table(pd.DataFrame({
        "Ação": ["Diversificação Vertical", "Hub de Dados Regional", "Green Tech Incentives"],
        "Objetivo": ["Atrair manufatura leve (pré-moldados tech)", "Treinamento em IA/IoT em parceria com Sorocaba", "Subsídios para indústrias Carbono Zero"],
        "Base de Dados": ["Treemap de Market Share", "Gráfico de Produtividade", "Análise de VAB Industrial"]
    }))

# --- RODAPÉ ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="footer">
        Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote. <br>
        <b>Instituição: Fatec Votorantim</b> | Relatório gerado em {datetime.now().strftime('%d/%m/%Y')}
    </div>
    """, unsafe_allow_html=True)
