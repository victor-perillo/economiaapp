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
    </small></p>
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO E TRATAMENTO DE DADOS ---
@st.cache_data
def load_and_clean_data():
    # Dados de Segmentos (Fonte: SEADE) [cite: 15, 19]
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5],
        'Dificuldade_40': [70, 60, 45, 85, 50], # Escala de dificuldade de implementação (%)
        'Ganho_Eficiencia': [15, 22, 18, 10, 12] # Ganho estimado com inovação (%)
    })
    
    # Histórico de Produtividade (Fonte: IBGE/CAGED) [cite: 18, 20]
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'Produtividade': [175, 190, 214, 223, 238, 255], # R$ Mil por trabalhador [cite: 122]
        'VAB_Indústria': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Serviços': [2100, 2250, 2380, 2750, 3100, 3500]
    })
    
    return df_seg, df_hist

df_seg, df_hist = load_and_clean_data()

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.title("🏭 BI Industrial")
    menu = st.radio("Etapas do Estudo:", 
                   ["Introdução", "Metodologia (ETL)", "Panorama Econômico", "Indústria 4.0 & Inovação", "Plano Estratégico"])
    st.divider()
    st.markdown("**Fontes de Dados:**")
    st.caption("IBGE Cidades, SEADE SP, Novo CAGED.")

# --- 1. INTRODUÇÃO ---
if menu == "Introdução":
    st.markdown('<p class="section-title">Cenário e Contexto Econômico</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="intro-box">', unsafe_allow_html=True)
    st.markdown(f"""
    Votorantim/SP possui um **legado industrial robusto**, historicamente alicerçado na indústria de base (cimento e metalurgia)[cite: 7]. 
    Entretanto, os dados revelam uma transição econômica latente: a indústria vem perdendo espaço para o setor de **Serviços**, 
    caracterizando um movimento de desindustrialização ou modernização da matriz[cite: 8].
    
    <span class="highlight">O Efeito Shadowing:</span> A proximidade com Sorocaba gera uma sombra econômica. 
    Enquanto a vizinha absorve indústrias de <span class="highlight">Alto Valor Agregado</span> (Tech/Automotiva), 
    Votorantim retém setores de baixo valor e alto impacto ambiental[cite: 9, 10].
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("🎯 **Desafio Central:** Migrar de uma economia de 'poeira' para uma economia de 'dados', atualizando o currículo técnico da população e atraindo demanda tecnológica[cite: 12].")

# --- 2. METODOLOGIA (ETL) ---
elif menu == "Metodologia (ETL)":
    st.markdown('<p class="section-title">Processamento de Dados (ETL)</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛠️ Transformação e Limpeza")
        st.write("- **Filtro de Nulos:** Remoção de anos sem consolidação do PIB (lag de 2 anos do IBGE)[cite: 18].")
        st.write("- **Padronização CNAE:** Unificação de nomenclaturas entre CAGED e SEADE (ex: Cimento -> Minerais Não Metálicos)[cite: 19].")
        st.write("- **Unificação (Join):** Cruzamento das bases de Emprego e PIB via Código de Município[cite: 20].")
    
    with c2:
        st.markdown("### 📊 Estrutura de Carga")
        st.write("- **DataFrames:** Dados estruturados em Pandas para análise imediata[cite: 22].")
        st.write("- **Formatos:** Exportação pronta para consumo em bibliotecas como Plotly e Matplotlib[cite: 22].")

# --- 3. PANORAMA ECONÔMICO ---
elif menu == "Panorama Econômico":
    st.markdown('<p class="section-title">Análise de VAB e Mercado</p>', unsafe_allow_html=True)
    
    col_vab1, col_vab2 = st.columns([0.6, 0.4])
    
    with col_vab1:
        fig_comp = px.line(df_hist, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'], markers=True,
                          title="Transição de Matriz: Crescimento Acelerado de Serviços",
                          color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"})
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("Nota-se que enquanto a Indústria mantém estabilidade, o setor de Serviços acelera a partir de 2021[cite: 68].")

    with col_vab2:
        fig_donut = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4,
                          title="Dominância do Setor de Cimento",
                          color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.write("O segmento de **Minerais Não Metálicos** detém mais de 55% da riqueza industrial local[cite: 107].")

# --- 4. INDÚSTRIA 4.0 & INOVAÇÃO ---
elif menu == "Indústria 4.0 & Inovação":
    st.markdown('<p class="section-title">Diagnóstico de Maturidade Digital</p>', unsafe_allow_html=True)
    
    st.markdown("""
    A transição para a **Gestão 4.0** em Votorantim é impulsionada pela necessidade de eficiência energética e redução de paradas não programadas (downtime)[cite: 137, 139].
    """)
    
    c_40_1, c_40_2 = st.columns(2)
    
    with c_40_1:
        st.markdown("#### Matriz: Dificuldade vs. Ganho de Operação")
        fig_scatter = px.scatter(df_seg, x='Dificuldade_40', y='Ganho_Eficiencia', 
                                 size='VAB_Pct', color='Segmento', text='Segmento',
                                 labels={'Dificuldade_40': 'Dificuldade de Implementação (%)', 'Ganho_Eficiencia': 'Ganho em Eficiência (%)'},
                                 title="Oportunidade de Inovação por Setor")
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("O setor de Alimentos apresenta maior dificuldade (gargalo de rastreabilidade), enquanto a Metalurgia tem maior potencial de ganho rápido.")

    with c_40_2:
        st.markdown("#### Eficiência: Valor Gerado por Trabalhador")
        fig_prod = px.bar(df_hist.tail(4), x='Ano', y='Produtividade', 
                         title="Produtividade Crescente (R$ Mil/Trabalhador)",
                         color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
        st.write("**Evidência:** O aumento da produtividade indica que as empresas estão investindo em tecnologia e automação para produzir mais com menos pessoas.")

# --- 5. PLANO ESTRATÉGICO ---
elif menu == "Plano Estratégico":
    st.markdown('<p class="section-title">Estratégia de Diversificação e Futuro</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="intro-box">', unsafe_allow_html=True)
    st.markdown("""
    O **Plano de Ação** visa mitigar o "Risco de Setor Único"[cite: 111]. Atualmente, a cidade é extremamente dependente de poucos players gigantes, 
    o que torna a economia vulnerável a choques no setor de construção civil[cite: 81, 82, 112]. 
    
    A estratégia propõe uma <span class="highlight">Diversificação Vertical</span>: em vez de apenas exportar cimento bruto, atrair indústrias de 
    manufatura leve que utilizem esse insumo para criar produtos de alto valor (como pré-moldados tecnológicos e impressão 3D de concreto).
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
    fig_meta.update_layout(barmode='group', title="Planejamento: Diversificação da Matriz Industrial")
    st.plotly_chart(fig_meta, use_container_width=True)

    st.markdown("### Eixos de Implementação")
    st.table(pd.DataFrame({
        "Ação Principal": ["Hub de Dados Regional", "Green Tech Incentives", "Requalificação 4.0"],
        "Como Funciona": [
            "Parceria com Sorocaba para criar um centro de IA focado em manutenção preditiva industrial.",
            "Subsídios fiscais para indústrias que adotarem créditos de carbono e energia limpa (IoT em fornos).",
            "Atualização do currículo técnico local para suprir o gap de analistas de dados industriais[cite: 84, 85]."
        ]
    }))

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Desenvolvido por:</b> Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p><b>Instituição:</b> Fatec Votorantim | Dados Extraídos de Fontes Públicas (IBGE/SEADE/CAGED)</p>
        <p><small>Relatório Gerado em {datetime.now().strftime('%d/%m/%Y')} | Observatório de Dados Industriais</small></p>
    </div>
    """, unsafe_allow_html=True)
