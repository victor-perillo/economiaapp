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
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .section-title { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; font-size: 24px; }
    .intro-box { background-color: #ffffff; padding: 25px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 25px; line-height: 1.6; }
    .footer { width: 100%; background-color: #ffffff; color: #444; text-align: center; padding: 30px; border-top: 1px solid #ddd; margin-top: 50px; }
    .highlight { color: #1E3A8A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO E TRATAMENTO DE DADOS ---
@st.cache_data
def load_and_clean_data():
    # Dados de Segmentos baseados no estudo setorial
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], 
        'Ganho_Eficiencia': [15, 22, 18, 10, 12]
    })
    
    # Histórico de Produtividade
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'Produtividade': [175, 190, 214, 223, 238, 255], 
        'VAB_Indústria': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Serviços': [2100, 2250, 2380, 2750, 3100, 3500]
    })
    
    return df_seg, df_hist

df_seg, df_hist = load_and_clean_data()

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.title("📊 BI Industrial")
    menu = st.radio("Etapas do Estudo:", 
                   ["Introdução", "Metodologia (ETL)", "Panorama Econômico", "Indústria 4.0 & Inovação", "Plano Estratégico"])
    st.divider()
    st.markdown("**Fontes de Dados:**")
    st.caption("IBGE Cidades, SEADE SP, Novo CAGED.")

# --- 1. INTRODUÇÃO ---
if menu == "Introdução":
    st.markdown('<p class="section-title">Cenário e Contexto Econômico</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="intro-box">', unsafe_allow_html=True)
    st.markdown("""
    Votorantim/SP possui um **legado industrial robusto** focado em indústria de base. 
    Entretanto, os dados revelam uma transição econômica latente: a indústria vem perdendo participação para o setor de **Serviços**, 
    caracterizando um movimento de desindustrialização ou modernização da matriz.
    
    <span class="highlight">O Efeito Shadowing:</span> A proximidade com Sorocaba gera uma sombra econômica. 
    Enquanto a vizinha atrai indústrias de **Alto Valor Agregado** (Tecnologia/Automotiva), 
    Votorantim historicamente retém setores de base e alto impacto ambiental.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("🎯 **Desafio Central:** Migrar de uma economia de manufatura tradicional para uma economia de dados, atualizando o currículo técnico da população e atraindo demanda tecnológica.")

# --- 2. METODOLOGIA (ETL) ---
elif menu == "Metodologia (ETL)":
    st.markdown('<p class="section-title">Processamento de Dados (ETL)</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛠️ Transformação e Limpeza")
        st.write("- **Filtro de Nulos:** Remoção de registros onde o PIB ainda não foi consolidado.")
        st.write("- **Padronização CNAE:** Unificação de nomenclaturas entre CAGED e SEADE para garantir integridade.")
        st.write("- **Unificação (Join):** Cruzamento das bases de Emprego e PIB utilizando o Código de Município como chave primária.")
    
    with c2:
        st.markdown("### 📊 Estrutura de Carga")
        st.write("- **DataFrames:** Dados estruturados em Pandas para análise imediata.")
        st.write("- **Visualização:** Uso de bibliotecas gráficas para consumo imediato no dashboard.")

# --- 3. PANORAMA ECONÔMICO ---
elif menu == "Panorama Econômico":
    st.markdown('<p class="section-title">Análise de VAB e Mercado</p>', unsafe_allow_html=True)
    
    col_vab1, col_vab2 = st.columns([0.6, 0.4])
    
    with col_vab1:
        fig_comp = px.line(df_hist, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'], markers=True,
                          title="Transição de Matriz: Crescimento Acelerado de Serviços",
                          color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"})
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("Nota-se que enquanto a Indústria cresce de forma constante, o setor de Serviços apresenta uma aceleração mais expressiva.")

    with col_vab2:
        fig_donut = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4,
                          title="Dominância Setorial (CNAE)",
                          color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.write("O setor de **Cimento e Minerais** permanece como o motor da cidade, detendo 55% da riqueza industrial.")

# --- 4. INDÚSTRIA 4.0 & INOVAÇÃO ---
elif menu == "Indústria 4.0 & Inovação":
    st.markdown('<p class="section-title">Diagnóstico de Maturidade Digital e Ganhos</p>', unsafe_allow_html=True)
    
    st.markdown("""
    As indústrias de Votorantim já operam em uma transição para a **Gestão 4.0**. 
    O principal diferencial é o uso da inovação através de **Sensoriamento (IoT)** em fornos e moendas, reduzindo o tempo de inatividade e otimizando o consumo energético.
    """)
    
    c_40_1, c_40_2 = st.columns(2)
    
    with c_40_1:
        st.markdown("#### Matriz: Dificuldade vs. Ganho de Operação")
        fig_scatter = px.scatter(df_seg, x='Dificuldade_40', y='Ganho_Eficiencia', 
                                 size='VAB_Pct', color='Segmento', text='Segmento',
                                 labels={'Dificuldade_40': 'Dificuldade de Implementação (%)', 'Ganho_Eficiencia': 'Ganho em Eficiência (%)'},
                                 title="Potencial de Modernização")
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.write("**Dificuldade:** O setor de Alimentos enfrenta gargalos de rastreabilidade, enquanto a metalurgia foca em integração de cadeia.")

    with c_40_2:
        st.markdown("#### Ganho de Operação: Produtividade por Trabalhador")
        fig_prod = px.bar(df_hist.tail(4), x='Ano', y='Produtividade', 
                         title="Valor Gerado (R$ Mil/Trabalhador)",
                         color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
        st.info("A produtividade cresce acima do ritmo de contratação, indicando que a indústria está produzindo mais através de tecnologia e automação.")

# --- 5. PLANO ESTRATÉGICO ---
elif menu == "Plano Estratégico":
    st.markdown('<p class="section-title">Estratégia de Diversificação e Portfólio Industrial</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="intro-box">', unsafe_allow_html=True)
    st.markdown("""
    O problema central identificado é a **Alta dependência econômica** de um único segmento. 
    Para mitigar esse risco sistêmico, o plano propõe atrair indústrias de manufatura leve que utilizem o cimento/cal local como insumo (Verticalização).
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    meta_df = pd.DataFrame({
        'Setor': ["Cimento", "Metalurgia", "Novas Techs", "Outros"],
        'Atual': [55, 20, 5, 20],
        'Meta': [40, 20, 25, 15]
    })
    
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(name='Cenário Atual', x=meta_df['Setor'], y=meta_df['Atual'], marker_color='#1E3A8A'))
    fig_meta.add_trace(go.Bar(name='Meta Plano de Ação', x=meta_df['Setor'], y=meta_df['Meta'], marker_color='#FF8C00'))
    fig_meta.update_layout(barmode='group', title="Diversificação de Mercado: Reduzindo a Dependência Industrial")
    st.plotly_chart(fig_meta, use_container_width=True)

    st.markdown("### Execução do Plano")
    st.write("A transição para um modelo sustentável exige três pilares baseados em dados:")
    
    st.table(pd.DataFrame({
        "Ação": ["Hub de Dados Regional", "Incentivos Green Tech", "Diversificação Vertical"],
        "Descrição": [
            "Centro de treinamento em IA para requalificar o operário local e reduzir o gap de habilidades.",
            "Subsídios fiscais para indústrias que utilizem créditos de carbono e energia limpa.",
            "Atração de indústrias de pré-moldados tecnológicos para agregar valor ao insumo básico da região."
        ]
    }))

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Desenvolvido por:</b> Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p><b>Instituição:</b> Fatec Votorantim | Disciplina: Análise de Dados Econômicos</p>
        <p><small>Relatório Gerado em {datetime.now().strftime('%d/%m/%Y')} | Dados Reais Consolidados</small></p>
    </div>
    """, unsafe_allow_html=True)
