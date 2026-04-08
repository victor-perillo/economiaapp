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

# --- ESTILO CSS CUSTOMIZADO (MODERNO) ---
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

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    # Dados de Segmentos baseados no anexo (Páginas 4 e 7)
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], 
        'Ganho_Eficiencia': [15, 22, 18, 10, 12],
        'Maturidade_Atual': [2.4, 3.1, 2.8, 1.9, 2.5] 
    })
    
    # Histórico de Produtividade (Páginas 5 e 7)
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

if ano_selecionado == "Todos":
    df_hist_filtered = df_hist
else:
    df_hist_filtered = df_hist[df_hist['Ano'] == int(ano_selecionado)]

# --- 1. INTRODUÇÃO & CONTEXTO ---
if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Cenário e Contexto Econômico</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
        Votorantim/SP ainda carrega um <b>legacy industrial</b> muito forte, focado essencialmente em indústria de base como cimento e metalurgia[cite: 7]. 
        Entretanto, o dataset econômico revela uma transição clara: a indústria vem perdendo participação (share) no PIB para o setor de Serviços, 
        indicando um processo latente de desindustrialização ou mudança de matriz econômica[cite: 8].
        <br><br>
        <span class="highlight">O Efeito Shadowing:</span> O município vive sob a "sombra" econômica de Sorocaba[cite: 9]. 
        Enquanto a vizinha atrai indústrias de alto valor agregado (Tech e Automotiva), Votorantim retém setores de baixo valor agregado e 
        alto impacto ambiental.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Problemas Identificados</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Risco de Setor Único:** O ecossistema é extremamente dependente de poucos players gigantes. Se uma dessas verticais sofre um choque, o impacto é sistêmico[cite: 81, 82].")
        st.warning("**Conflito de Zoneamento:** O avanço imobiliário sobre áreas industriais cria barreiras para a expansão das fábricas (Trade-off expansão urbana vs. produção)[cite: 87, 88].")
    with c2:
        st.error("**Skill Gap (Mão de Obra):** Há um desalinhamento entre o perfil do trabalhador local e as demandas da Indústria 4.0. O mercado pede automação, mas a força ainda é analógica[cite: 84, 85].")
        st.info("**Dependência de 'Poeira':** Necessidade urgente de migrar para uma economia que gere mais dados e menos impacto ambiental.")

# --- 2. METODOLOGIA (ETL) ---
elif menu == "Metodologia (ETL)":
    st.markdown('<p class="section-title">Processamento de Dados (ETL)</p>', unsafe_allow_html=True)
    
    col_etl1, col_etl2 = st.columns(2)
    with col_etl1:
        st.markdown("### 📥 Extração & Transformação")
        st.write("**1. Fontes Governamentais:** Coleta via IBGE Cidades, SEADE e Novo CAGED[cite: 15].")
        st.write("**2. Limpeza de Nulos:** Remoção de registros incompletos, respeitando o lag de 2 anos do PIB municipal[cite: 18].")
        st.write("**3. Padronização:** Unificação de nomenclaturas (ex: 'CNAE Fabricação de Cimento' para 'Indústria de Minerais Não Metálicos')[cite: 19].")
    
    with col_etl2:
        st.markdown("### 🔄 Unificação & Carga")
        st.write("**4. Join Técnico:** Merge das bases utilizando o Ano e o Código de Município como chaves primárias[cite: 20].")
        st.write("**5. Estruturação:** Dados consolidados em DataFrames (Pandas) para visualização dinâmica via Plotly[cite: 22].")
        st.code("# Exemplo de Join\ndf_final = pd.merge(df_pib, df_emprego, on=['cod_mun', 'ano'])", language="python")

# --- 3. DASHBOARD EXECUTIVO ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macroeconômico Industrial</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("VAB Industrial", f"R$ {df_hist_filtered['VAB_Indústria'].iloc[-1]}M")
    with c2:
        st.metric("Produtividade Média", f"{df_hist_filtered['Produtividade'].mean():.1f}k")
    with c3:
        st.metric("Dominância Setorial", "55%", "Minerais")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist_filtered, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'],
                              title="Crescimento Setorial: Aceleração de Serviços [cite: 68]",
                              color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"}, markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Análise:</b> Enquanto a indústria cresce de forma constante, o setor de serviços acelera rapidamente, sinalizando a "terceirização" da economia local[cite: 68, 69].</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.5, title="Distribuição de VAB (CNAE) [cite: 25]")
        st.plotly_chart(fig_pizza, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Destaque:</b> O setor de Cimento e Minerais detém 55% da riqueza industrial, sendo o motor absoluto da cidade[cite: 106, 107].</div>', unsafe_allow_html=True)

# --- 4. INDÚSTRIA 4.0 ---
elif menu == "Análise de Maturidade 4.0":
    st.markdown('<p class="section-title">Diagnóstico Digital e Eficiência</p>', unsafe_allow_html=True)
    
    st.write("A indústria de Votorantim já opera em transição para a Gestão 4.0, especialmente no uso de **Sensoriamento (IoT)** para reduzir downtime em fornos[cite: 137, 139].")

    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_hist_filtered, x='Ano', y='Produtividade', title="Evolução da Produtividade (R$ por Trabalhador) [cite: 122]", color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Evidência:</b> O VAB por trabalhador cresce acima da contratação, provando que a indústria produz mais com tecnologia e automação[cite: 109, 138].</div>', unsafe_allow_html=True)

    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', name='Maturidade', marker=dict(color='#1E3A8A')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Índice de Maturidade Digital")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Nota:</b> Metalurgia lidera em integração, enquanto Alimentos possui o maior gap para automação plena.</div>', unsafe_allow_html=True)

# --- 5. PLANO DE AÇÃO ---
elif menu == "Plano de Ação":
    st.markdown('<p class="section-title">Estratégia de Diversificação e Portfólio Industrial</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><b>Problema Central:</b> Alta dependência econômica de um único segmento e risco de concentração sistêmica[cite: 155].</div>', unsafe_allow_html=True)

    # Gráfico de Metas
    meta_df = pd.DataFrame({
        'Setor': ["Cimento", "Metalurgia", "Novas Techs", "Outros"],
        'Cenário Atual': [55, 20, 5, 20],
        'Meta Plano': [40, 20, 25, 15]
    })
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(name='Atual', x=meta_df['Setor'], y=meta_df['Cenário Atual'], marker_color='#1E3A8A'))
    fig_meta.add_trace(go.Bar(name='Meta', x=meta_df['Setor'], y=meta_df['Meta Plano'], marker_color='#FF8C00'))
    st.plotly_chart(fig_meta, use_container_width=True)

    st.markdown("### 🚀 Ações Estratégicas Baseadas em Dados")
    
    # 5 Ações detalhadas
    st.table(pd.DataFrame({
        "Ação": [
            "1. Diversificação Vertical", 
            "2. Hub de Dados Regional", 
            "3. Green Tech Incentives",
            "4. Simbiose Industrial",
            "5. Requalificação 4.0"
        ],
        "Objetivo": [
            "Atrair indústrias de manufatura leve que utilizem o cimento/cal local como insumo (ex: pré-moldados tech).",
            "Criar centro de treinamento em IA e IoT em parceria com Sorocaba para suporte tecnológico.",
            "Subsídios fiscais para indústrias que utilizem créditos de carbono e energia limpa.",
            "Integrar o cluster de minerais com novas indústrias de reciclagem para reduzir impacto ambiental e gerar novos subprodutos.",
            "Atualização do currículo técnico da população para atrair empresas que gerem mais dados e 'menos poeira'."
        ]
    }))

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Observatório Industrial Votorantim v2.1</b> | Desenvolvido com base no Dataset Consolidado (IBGE/SEADE/CAGED)</p>
        <p>Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
