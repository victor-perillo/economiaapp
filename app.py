import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Observatório Industrial Votorantim",
    page_icon="🏭",
    layout="wide"
)

# --- ESTILO CSS PARA MELHOR LEITURA ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .section-title { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; font-size: 22px; }
    .intro-box { background-color: #e9ecef; padding: 20px; border-radius: 10px; border-left: 5px solid #1E3A8A; margin-bottom: 25px; }
    .footer { width: 100%; background-color: #ffffff; color: #444; text-align: center; padding: 30px; border-top: 1px solid #ddd; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS (DADOS REAIS CONSOLIDADOS) ---
@st.cache_data
def load_data():
    # Segmentos (Fonte: SEADE/VAB Municipal)
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos (Cimento)", "Metalurgia", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [55, 20, 12, 8, 5]
    })
    
    # Histórico (Fonte: IBGE/CAGED)
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
        'VAB_Indústria': [1520, 1610, 1740, 1920, 2100, 2300],
        'VAB_Serviços': [2100, 2250, 2380, 2750, 3100, 3500],
        'Estoque_Emprego': [8450, 8120, 8600, 8750, 8920, 9100],
        'Produtividade': [175, 190.5, 214.2, 223.2, 235.0, 250.0] # R$ Mil/Trabalhador
    })
    
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 Navegação")
    menu = st.radio("Selecione a Etapa:", 
                   ["Introdução", "Processo ETL", "Panorama Econômico", "Diagnóstico e Risco", "Plano Estratégico"])
    st.divider()
    st.markdown("**Fontes Oficiais:**")
    st.caption("IBGE Cidades, SEADE, Novo CAGED.")

# --- 1. INTRODUÇÃO ---
if menu == "Introdução":
    st.markdown('<p class="section-title">Cenário Econômico e Industrial</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="intro-box">', unsafe_allow_html=True)
    st.markdown("""
    Votorantim ainda carrega um **legacy industrial muito forte**, focado em indústria de base como cimento e metalurgia[cite: 7]. 
    No entanto, o dataset econômico mostra uma transição clara: a indústria está perdendo share no PIB para o setor de Serviços, 
    indicando um processo de desindustrialização ou mudança de matriz econômica[cite: 8].
    
    O cenário sugere que o município vive um efeito de **"Shadowing" de Sorocaba**[cite: 9]. Enquanto a vizinha atrai indústrias 
    de alto valor agregado (Tech e Automotiva), Votorantim mantém setores de baixo valor agregado e alto impacto ambiental[cite: 10].
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Insight:** Para reverter esse quadro, é necessária uma atualização urgente no currículo técnico para atrair empresas que gerem mais dados e menos poeira[cite: 12].")
    with col2:
        st.success("🎯 **Objetivo:** Analisar a saúde econômica através de dados e propor caminhos para a Indústria 4.0.")

# --- 2. PROCESSO ETL ---
elif menu == "Processo ETL":
    st.markdown('<p class="section-title">Engenharia de Dados (ETL)</p>', unsafe_allow_html=True)
    
    col_etl1, col_etl2 = st.columns([1, 1])
    
    with col_etl1:
        st.markdown("### 📥 Extração")
        st.write("- **Fontes:** IBGE Cidades (PIB), SEADE (VAB) e Novo CAGED (Empregos)[cite: 15].")
        st.write("- **Formatos:** Extração via APIs (SIDRA/IBGE) e arquivos CSV/JSON[cite: 16].")
        
        st.markdown("### ⚙️ Transformação")
        st.write("- **Limpeza:** Tratamento de registros incompletos e defasagem de 2 anos do PIB municipal[cite: 18].")
        st.write("- **Padronização:** Unificação de CNAEs (Ex: 'Fabricação de Cimento' consolidado em 'Minerais Não Metálicos')[cite: 19].")
        st.write("- **Unificação:** Join das bases utilizando o Código de Município como chave primária[cite: 20].")

    with col_etl2:
        st.markdown("### 📤 Carga")
        st.code("""
# Exemplo de Carga no DataFrame
df_final = pd.merge(df_pib, df_emprego, on='ano')
df_final.to_csv('votorantim_consolidado.csv')
        """, language='python')
        st.write("Os dados limpos foram estruturados em DataFrames (Pandas) para visualização imediata com Plotly no ambiente de análise[cite: 22].")

# --- 3. PANORAMA ECONÔMICO ---
elif menu == "Panorama Econômico":
    st.markdown('<p class="section-title">Participação Setorial e Crescimento</p>', unsafe_allow_html=True)
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Líder Industrial", "Cimento", "55% do VAB")
    c2.metric("Postos de Trabalho", "9.100", "+2.0%")
    c3.metric("Status", "Em Transição", "Indústria → Serviços")

    col_g1, col_g2 = st.columns([0.6, 0.4])
    
    with col_g1:
        st.markdown("#### Evolução Comparativa: Indústria vs Serviços")
        fig_evol = px.line(df_hist, x='Ano', y=['VAB_Indústria', 'VAB_Serviços'], markers=True,
                          labels={'value': 'R$ Milhões', 'variable': 'Setor'},
                          color_discrete_map={"VAB_Indústria": "#1E3A8A", "VAB_Serviços": "#FF8C00"})
        st.plotly_chart(fig_evol, use_container_width=True)
        st.caption("O setor de Serviços está acelerando muito mais rápido que a indústria[cite: 68].")

    with col_g2:
        st.markdown("#### Composição Industrial (CNAE)")
        fig_pie = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4,
                        color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.write("O maior segmento industrial é a Fabricação de Minerais Não Metálicos (Cimento)[cite: 45].")

# --- 4. DIAGNÓSTICO E RISCO ---
elif menu == "Diagnóstico e Risco":
    st.markdown('<p class="section-title">Saúde do Setor e Identificação de Gargalos</p>', unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown("#### Produtividade e Eficiência")
        fig_prod = px.bar(df_hist.tail(4), x='Ano', y='Produtividade', 
                         title="R$ Mil Gerados por Trabalhador", color_discrete_sequence=['#008080'])
        st.plotly_chart(fig_prod, use_container_width=True)
        st.write("**Eficiência:** A saída financeira cresce acima da contratação, indicando adoção de automação[cite: 109, 138].")

    with col_r2:
        st.error("⚠️ **Principais Riscos Identificados**")
        st.markdown("""
        1. **Dependência de Poucos Players:** Ecossistema muito dependente do Grupo Votorantim[cite: 81].
        2. **Risco de Setor Único:** Crises na construção civil impactam a cidade inteira simultaneamente[cite: 112].
        3. **Skill Gap:** Força de trabalho ainda atrelada a processos manuais, enquanto o mercado pede dados[cite: 85].
        4. **Conflito Urbano:** Avanço imobiliário sobre áreas industriais limita a expansão das fábricas[cite: 87, 88].
        """)

# --- 5. PLANO ESTRATÉGICO ---
elif menu == "Plano Estratégico":
    st.markdown('<p class="section-title">Estratégias Baseadas em Evidências</p>', unsafe_allow_html=True)
    
    # Gráfico de Metas conforme Página 9 do PDF
    meta_df = pd.DataFrame({
        'Setor': ["Cimento", "Metalurgia", "Novas Techs", "Outros"],
        'Atual': [55, 20, 5, 20],
        'Meta': [40, 20, 25, 15]
    })
    
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(name='Cenário Atual', x=meta_df['Setor'], y=meta_df['Atual'], marker_color='#1E3A8A'))
    fig_meta.add_trace(go.Bar(name='Meta Plano de Ação', x=meta_df['Setor'], y=meta_df['Meta'], marker_color='#FF8C00'))
    fig_meta.update_layout(barmode='group', title="Diversificação do Portfólio Industrial (%)")
    st.plotly_chart(fig_meta, use_container_width=True)

    st.markdown("### Matriz de Ação")
    st.table(pd.DataFrame({
        "Ação": ["Diversificação Vertical", "Hub de Dados Regional", "Green Tech Incentives"],
        "Objetivo": [
            "Atrair manufatura leve que use o cimento local como insumo[cite: 141].",
            "Centro de treinamento em IA para requalificar o operário[cite: 141].",
            "Subsídios para indústrias com energia limpa e créditos de carbono[cite: 141]."
        ]
    }))

# --- FINALIZAÇÃO / FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p><b>Desenvolvido por:</b> Bruno V. Queiroz, Gislaine Takushi, Mariana Lima, Victor Perillo e Vinicius Pierote.</p>
        <p><b>Instituição:</b> Fatec Votorantim | Disciplina: Economia e Análise de Dados</p>
        <hr>
        <p><small>Relatório gerado em {datetime.now().strftime('%d/%m/%Y')} | Dados Reais Consolidados (IBGE/SEADE/CAGED)</small></p>
    </div>
    """, unsafe_allow_html=True)
