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
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], 
        'Ganho_Eficiencia': [15, 22, 18, 10, 12],
        'Maturidade_Atual': [2.4, 3.1, 2.8, 1.9, 2.5] # Escala 1 a 5
    })
    
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
    
    # SELETOR DE DATA
    anos_disponiveis = ["Todos"] + [str(ano) for ano in df_hist['Ano'].unique()]
    ano_selecionado = st.selectbox("Selecione o Período de Análise:", anos_disponiveis)
    
    st.divider()
    menu = st.radio("Navegação Estratégica:", 
                   ["Dashboard Executivo", "Análise de Maturidade 4.0", "Plano de Reindustrialização"])

# Filtragem dos dados baseada no seletor
if ano_selecionado == "Todos":
    df_hist_filtered = df_hist
else:
    df_hist_filtered = df_hist[df_hist['Ano'] == int(ano_selecionado)]

# --- 1. DASHBOARD EXECUTIVO ---
if menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macroeconômico Industrial</p>', unsafe_allow_html=True)
    
    # KPIs Rápidos
    c1, c2, c3 = st.columns(3)
    with c1:
        vab_total = df_hist_filtered['VAB_Indústria'].sum()
        st.metric("VAB Industrial Acumulado", f"R$ {vab_total}M")
    with c2:
        prod_media = round(df_hist_filtered['Produtividade'].mean(), 2)
        st.metric("Produtividade Média", f"{prod_media} pts")
    with c3:
        crescimento = round(((df_hist['VAB_Indústria'].iloc[-1] / df_hist['VAB_Indústria'].iloc[0]) - 1) * 100, 1)
        st.metric("Crescimento 5 Anos", f"{crescimento}%", "+5.2%")

    col_left, col_right = st.columns([0.6, 0.4])

    with col_left:
        fig_evolucao = px.area(df_hist_filtered, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'],
                              title="Convergência Setorial: Indústria vs Serviços",
                              color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"},
                              line_shape='spline')
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Análise:</b> O gráfico revela um fenômeno de "terceirização avançada". Enquanto o valor industrial cresce nominalmente, sua participação relativa encolhe perante serviços, exigindo uma integração urgente entre produto e serviço (Servitização).</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.5,
                          title="Concentração de Riqueza por CNAE",
                          color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pizza, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Destaque:</b> 55% da economia industrial depende de Minerais Não Metálicos. Esta dependência cria um risco de exposição a ciclos da construção civil.</div>', unsafe_allow_html=True)

# --- 2. INDÚSTRIA 4.0 (MELHORADO) ---
elif menu == "Análise de Maturidade 4.0":
    st.markdown('<p class="section-title">Diagnóstico de Inteligência 4.0</p>', unsafe_allow_html=True)
    
    # Explicação técnica
    st.write("""
    A transição para a Indústria 4.0 em Votorantim não é apenas sobre robôs, mas sobre a **Digitalização do Chão de Fábrica**. 
    Abaixo, analisamos onde o investimento tecnológico gera o maior retorno sobre o capital investido (ROIC).
    """)

    c1, c2 = st.columns(2)
    
    with c1:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=df_seg['Maturidade_Atual'],
            theta=df_seg['Segmento'],
            fill='toself',
            name='Nível de Maturidade',
            marker=dict(color='#1E3A8A')
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                              title="Índice de Maturidade Digital por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Insight:</b> O setor metalúrgico lidera a maturidade digital local. O setor de Alimentos apresenta o maior gap tecnológico, sendo a principal oportunidade para consultorias de automação.</div>', unsafe_allow_html=True)

    with c2:
        fig_bubbles = px.scatter(df_seg, x='Dificuldade_40', y='Ganho_Eficiencia',
                                size='VAB_Pct', color='Segmento',
                                title="Matriz de Priorização Tecnológica",
                                labels={'Dificuldade_40': 'Barreira de Implementação', 'Ganho_Eficiencia': 'ROI Estimado'})
        st.plotly_chart(fig_bubbles, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Estratégia:</b> Setores no quadrante superior esquerdo são "Quick Wins" (Baixo esforço/Alto ganho). Deve-se focar em sensores IoT para manutenção preditiva em plantas de moagem.</div>', unsafe_allow_html=True)

# --- 3. PLANO ESTRATÉGICO (MODERNIZADO) ---
elif menu == "Plano de Reindustrialização":
    st.markdown('<p class="section-title">Eixo Estratégico 2024-2030</p>', unsafe_allow_html=True)
    
    st.info("💡 **Visão de Futuro:** Transformar Votorantim de um polo de extração para um polo de manufatura avançada e materiais sustentáveis.")

    tab1, tab2 = st.tabs(["Metas de Diversificação", "Pilares de Ação"])
    
    with tab1:
        meta_df = pd.DataFrame({
            'Setor': ["Cimento/Base", "Materiais Avançados", "AgroTech", "Serviços Industriais"],
            'Cenário Atual': [60, 10, 5, 25],
            'Meta 2030': [35, 30, 15, 20]
        })
        fig_metas = go.Figure()
        fig_metas.add_trace(go.Bar(name='Cenário Atual', x=meta_df['Setor'], y=meta_df['Cenário Atual'], marker_color='#1E3A8A'))
        fig_metas.add_trace(go.Bar(name='Meta 2030', x=meta_df['Setor'], y=meta_df['Meta 2030'], marker_color='#FF8C00'))
        st.plotly_chart(fig_metas, use_container_width=True)
        st.markdown('<div class="chart-caption"><b>Objetivo:</b> Reduzir a dependência do cimento básico em 25% e migrar para "Materiais Avançados" (grafeno, polímeros técnicos), aproveitando a infraestrutura logística existente.</div>', unsafe_allow_html=True)

    with tab2:
        st.write("### 🚀 Pilares de Execução")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.subheader("1. Simbiose Industrial")
            st.write("Criar um ecossistema onde o resíduo da metalurgia sirva de insumo para a construção civil, reduzindo custos e pegada de carbono.")
        with col_p2:
            st.subheader("2. Sandbox Tecnológico")
            st.write("Atrair startups de Sorocaba para testar soluções de IA e Robótica nas plantas de Votorantim com incentivos fiscais específicos.")
        with col_p3:
            st.subheader("3. Talent Hub")
            st.write("Parceria com Fatec e Senai para criação de cursos focados em Data Science aplicado à manufatura e operação de drones industriais.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Observatório Industrial Votorantim v2.0</b> - Inteligência de Dados Aplicada</p>
        <p>Desenvolvido por: Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p>Relatório dinâmico gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
