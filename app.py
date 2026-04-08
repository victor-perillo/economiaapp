import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial | Votorantim SP",
    page_icon="🏭",
    layout="wide"
)

# --- ESTILO CSS AVANÇADO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .card { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .section-title { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; margin-top: 20px; }
    .footer { position: relative; width: 100%; background-color: #f1f3f5; color: #444; text-align: center; padding: 20px; font-size: 14px; margin-top: 50px; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS (ETL CONFORME PDF) ---
@st.cache_data
def get_data():
    # Estrutura baseada nos dados consolidados do PDF [cite: 15, 16]
    df_seg = pd.DataFrame({
        'Segmento': ["Cimento/Minerais", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Cor': ['#1E3A8A', '#2E59A8', '#4A7CC2', '#769FDB', '#A3C1F3']
    })
    
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'VAB_Ind': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Ser': [2100, 2250, 2380, 2750, 3100, 3500],
        'Empregos': [8450, 8120, 8600, 8750, 8920, 9100] # Baseado no gráfico de estoque [cite: 76]
    })
    
    return df_seg, df_hist

df_seg, df_hist = get_data()

# --- HEADER ---
st.title("🏭 Observatório de Inteligência Industrial")
st.markdown("### Análise Econômica e Transição para Indústria 4.0 - Votorantim/SP")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2761/2761014.png", width=80)
    st.header("Menu de Navegação")
    aba = st.radio("Escolha uma visão:", ["Metodologia ETL", "Panorama Econômico", "Diagnóstico & Risco", "Plano Estratégico"])
    
    st.divider()
    st.info("**Fontes Governamentais:**\n- IBGE (SIDRA)\n- SEADE\n- Novo CAGED")

# --- ABA 1: METODOLOGIA ETL ---
if aba == "Metodologia ETL":
    st.subheader("⚙️ Pipeline de Dados (ETL)")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Extração** [cite: 14]")
        st.caption("Coleta de dados brutos de fontes distintas como IBGE (PIB), SEADE (VAB) e CAGED (Empregos) em formatos CSV, XML e JSON[cite: 15, 16].")
    with c2:
        st.markdown("**2. Transformação** [cite: 17]")
        st.caption("Limpeza de nulos (tratando o lag de 2 anos do PIB), padronização de nomenclaturas CNAE e unificação (Join) das bases via código de município[cite: 18, 19, 20].")
    with c3:
        st.markdown("**3. Carga** [cite: 21]")
        st.caption("Estruturação dos dados em DataFrames (Pandas) prontos para visualização em bibliotecas como Plotly e Matplotlib[cite: 22].")

# --- ABA 2: PANORAMA ECONÔMICO ---
elif aba == "Panorama Econômico":
    # KPIs Rápidos
    m1, m2, m3 = st.columns(3)
    m1.metric("Líder de VAB", "Cimento (55%)", "Dominância Industrial")
    m2.metric("Tendência", "Setor de Serviços", "Crescimento Acelerado")
    m3.metric("Recuperação Post-Pandemia", "Resiliente", "Empregos ↑")

    st.markdown('<p class="section-title">Evolução do VAB e Setor de Serviços</p>', unsafe_allow_html=True)
    
    col_text, col_chart = st.columns([0.4, 0.6])
    with col_text:
        st.markdown("""
        **Transição de Matriz Econômica:**
        A cidade está deixando de ser apenas um "canteiro de fábricas" para se tornar um polo de serviços[cite: 69]. 
        
        **Efeito Shadowing (Sorocaba):**
        Votorantim enfrenta o desafio de reter indústrias de alto valor agregado, que hoje migram para a vizinha Sorocaba (Setor Tech/Automotivo), mantendo setores de alto impacto ambiental.
        """)
        st.warning("A indústria cresce de forma constante, mas o setor de serviços acelera mais rápido[cite: 68].")
        
    with col_chart:
        fig_evol = px.area(df_hist, x='Ano', y=['Indústria', 'Serviços'], 
                          title="Composição do VAB (Indústria vs Serviços) - R$ Milhões",
                          color_discrete_map={"Indústria": "#1E3A8A", "Serviços": "#FF8C00"})
        st.plotly_chart(fig_evol, use_container_width=True)

# --- ABA 3: DIAGNÓSTICO & RISCO ---
elif aba == "Diagnóstico & Risco":
    st.markdown('<p class="section-title">Análise de Risco e Produtividade</p>', unsafe_allow_html=True)
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("#### Concentração Industrial (VAB %)")
        fig_donut = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.5,
                          color_discrete_sequence=df_seg['Cor'])
        st.plotly_chart(fig_donut, use_container_width=True)
        st.error("**Risco de Setor Único:** A dependência extrema do cimento torna o PIB vulnerável a crises na construção civil.")

    with d2:
        st.markdown("#### Saúde do Emprego Industrial")
        fig_emp = px.line(df_hist, x='Ano', y='Empregos', markers=True, 
                          title="Estoque de Emprego Industrial (Resiliência)",
                          color_discrete_sequence=['#2E59A8'])
        st.plotly_chart(fig_emp, use_container_width=True)
        st.info("Mesmo com a queda em 2020, o setor recuperou e superou os níveis pré-crise[cite: 76].")

    st.divider()
    st.markdown("#### 🤖 Diagnóstico Indústria 4.0")
    st.write("A produtividade por trabalhador indica investimento em automação (produzir mais com menos pessoas)[cite: 109, 110].")
    st.markdown("""
    - **Skill Gap:** Desalinhamento entre o perfil manual do trabalhador local e a demanda por automação/dados[cite: 83, 85].
    - **Inovação:** Uso de IoT (Sensoriamento) em fornos para reduzir downtime e custos energéticos[cite: 139].
    """)

# --- ABA 4: PLANO ESTRATÉGICO ---
elif aba == "Plano Estratégico":
    st.markdown('<p class="section-title">Estratégias de Diversificação (Portfólio Industrial)</p>', unsafe_allow_html=True)
    
    # Gráfico de Meta conforme Página 9 do PDF
    meta_df = pd.DataFrame({
        'Setor': ["Cimento", "Metalurgia", "Novas Techs", "Outros"],
        'Atual': [55, 20, 5, 20],
        'Meta': [40, 20, 25, 15]
    })
    
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(name='Cenário Atual', x=meta_df['Setor'], y=meta_df['Atual'], marker_color='#1E3A8A'))
    fig_meta.add_trace(go.Bar(name='Meta Plano de Ação', x=meta_df['Setor'], y=meta_df['Meta'], marker_color='#FF8C00'))
    fig_meta.update_layout(barmode='group', title="Planejamento: Redução de Dependência e Novos Segmentos")
    st.plotly_chart(fig_meta, use_container_width=True)

    with st.expander("Ver Detalhes do Plano de Ação", expanded=True):
        st.table(pd.DataFrame({
            "Ação Estratégica": ["Diversificação Vertical", "Hub de Dados Regional", "Green Tech Incentives"],
            "Objetivo": [
                "Atrair manufatura leve que use insumos locais (cimento/cal)[cite: 141].",
                "Centro de treinamento em IA e IoT com foco em requalificação[cite: 141].",
                "Subsídios para indústrias com crédito de carbono e energia limpa[cite: 141]."
            ]
        }))

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Desenvolvido por:</b> Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p><b>Instituição:</b> Fatec Votorantim | Disciplina: Projeto Integrador</p>
        <p><small>Relatório gerado em {datetime.now().strftime('%d/%m/%Y')} baseado em evidências de datasets consolidados.</small></p>
    </div>
    """, unsafe_allow_html=True)
