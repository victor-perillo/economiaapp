# --- LOGICA DE NAVEGAÇÃO E DASHBOARD (SUBSTITUA A PARTIR DO PRIMEIRO "if menu == ") ---

if menu == "Introdução & Contexto":
    st.markdown('<p class="section-title">Contexto e Ordenamento Territorial</p>', unsafe_allow_html=True)
    
    tab_econ, tab_diretor = st.tabs(["📊 Análise Econômica", "📜 Plano Diretor de Votorantim"])
    
    with tab_econ:
        st.markdown("""
        <div class="card">
            <h3>Observatório Econômico Votorantim: Da Base Industrial à Inteligência de Dados</h3>
            Votorantim atravessa um momento crucial de transição econômica. Historicamente consolidada como um pilar da indústria de base (minerais e metalurgia), a cidade hoje apresenta uma nova dinâmica revelada pelos dados: a ascensão acelerada do setor de serviços e um aumento expressivo na produtividade por operário.
            <br><br>
            Este dashboard utiliza técnicas avançadas de Ciência de Dados para monitorar essa evolução, integrando fontes oficiais (IBGE, SEADE, CAGED) em um pipeline ETL automatizado. Nosso objetivo é fornecer uma visão estratégica sobre o fenômeno de <b>"Shadowing"</b> em relação a Sorocaba e identificar como a Indústria 4.0 pode atuar como o motor para a retenção de talentos e o crescimento do VAB municipal no próximo decênio.
        </div>
        """, unsafe_allow_html=True)

    with tab_diretor:
        st.markdown("""
        <div class="card">
            Votorantim possui um <b>Plano Diretor</b> que organiza o crescimento da cidade e define onde atividades industriais podem se instalar, sempre respeitando regras de uso do solo e exigências ambientais. Em teoria, o município permite a instalação de indústrias, desde que elas estejam localizadas nas zonas adequadas e atendam aos critérios legais.
            <br><br>
            Na prática, porém, o cenário atual cria dificuldades. As áreas industriais são limitadas e, com o crescimento da cidade, muitas delas passaram a ficar próximas ou até “encostadas” em regiões urbanas. Isso gera conflitos, pois aumenta a exigência por controle de impactos como ruído, trânsito de caminhões e poluição, restringindo principalmente a instalação de indústrias de maior porte.
            <br><br>
            Além disso, existem restrições ambientais importantes que reduzem ainda mais o espaço disponível, somadas a processos burocráticos e custos de adequação. O resultado é que, embora não haja proibição, há uma limitação prática: poucas áreas realmente viáveis e um nível alto de exigência para novos empreendimentos.
            <br><br>
            Em resumo, Votorantim permite a instalação de indústrias, mas o avanço urbano, as restrições ambientais e a escassez de zonas industriais adequadas tornam esse processo cada vez mais difícil, especialmente para empresas maiores ou com maior impacto.
            <br><br>
            <small>Fonte: <a href="https://www.votorantim.sp.gov.br/plano-diretor-lei-vigente-anexos" target="_blank">votorantim.sp.gov.br/plano-diretor</a></small>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Problemas Identificados":
    st.markdown('<p class="section-title">Matriz de Problemas</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.error("""**Clusterização e Dependência**: O ecossistema é muito dependente de poucos players gigantes (como o Grupo Votorantim). 
Em termos de risco de negócio, isso é perigoso: se uma dessas verticais sofre um choque, o impacto no município é sistêmico.""")
        st.warning("""**Conflito Territorial:** O avanço do setor imobiliário sobre áreas industriais cria barreiras para a escalabilidade das fábricas. 
É um problema de Trade-off entre expansão urbana e manutenção da produção.""")
    with c2:
        st.error("""**Skill Gap (Mão de Obra):** Há um desalinhamento entre o perfil do trabalhador local e as demandas da Indústria 4.0. 
Enquanto o mercado pede automação, a força de trabalho ainda está atrelada a processos manuais.""")
        st.info("""**Efeito Shadowing:** Ocorre quando Votorantim perde talentos e investimentos para Sorocaba. 
Isso resulta em uma economia local estagnada, focada em setores de baixo valor agregado ou indústrias de base.""")

elif menu == "Metodologia ETL":
    st.markdown('<p class="section-title">Pipeline de Dados (ETL)</p>', unsafe_allow_html=True)
    st.markdown('''
        <div class="step-box step-extracao">
            <b>1. Extração:</b><br>
            Ação: Coletamos dados brutos de três fontes governamentais distintas: IBGE Cidades (Séries históricas de PIB), SEADE (VAB por setor municipal) e Novo CAGED (Movimentação formal de empregos).<br>
            Formatos: CSV e consultas em tabelas do SIDRA/IBGE.
        </div>
        <div class="step-box step-transformacao">
            <b>2. Transformação:</b><br>
            Limpeza de Nulos: Removemos registros incompletos.<br>
            Padronização: Unificamos nomenclaturas CNAE e escalas financeiras (Mi/Bi).<br>
            Unificação (Join): Merge das bases de Emprego e PIB utilizando o Ano como chave primária.
        </div>
        <div class="step-box step-carga">
            <b>3. Carregamento:</b><br>
            Ação: O dataset limpo foi estruturado em DataFrames e exportado para formatos prontos para consumo no Streamlit.
        </div>
    ''', unsafe_allow_html=True)

elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    delta_yoy = None
    if ano_selecionado != "Todos":
        idx = df_hist[df_hist['Ano'] == int(ano_selecionado)].index[0]
        if idx > 0:
            pib_ant = df_hist.iloc[idx-1]['PIB']
            delta_yoy = f"{((dados_atuais['PIB']/pib_ant)-1)*100:.1f}% vs ano anterior"
    
    pib_2018 = df_hist.iloc[0]['PIB']
    perc_acumulado = ((dados_atuais['PIB']/pib_2018)-1)*100

    with c1:
        st.metric(f"PIB Municipal ({ano_txt})", formatar_valor(dados_atuais['PIB']), delta=delta_yoy)
        st.markdown(f'<p class="acumulado-text">🚀 Acumulado: <b>+{perc_acumulado:.1f}%</b> desde 2018</p>', unsafe_allow_html=True)
        
    with c2:
        st.metric("VAB Indústria", formatar_valor(dados_atuais['VAB_Industria']))
    with c3:
        st.metric("VAB Serviços", formatar_valor(dados_atuais['VAB_Servicos']))
    with c4:
        st.metric("Produtividade", f"R$ {dados_atuais['Produtividade']}k")

    # --- INSERÇÃO DO BOTÃO IPCA E LÓGICA ---
    st.markdown("---")
    if st.button("Inserir IPCA"):
        ipca_votorantim = {
            2018: 3.75, 2019: 4.31, 2020: 4.52, 2021: 10.06, 
            2022: 5.79, 2023: 4.62, 2024: 4.50, 2025: 4.00
        }
        
        if ano_selecionado == "Todos":
            st.info("Selecione um ano na barra lateral para ver o IPCA correspondente.")
        else:
            valor_ipca = ipca_votorantim.get(int(ano_selecionado), 0)
            st.write(f"**IPCA Votorantim ({ano_selecionado}):** {valor_ipca}%")
    st.markdown("---")

    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist, x='Ano', y=['VAB_Industria', 'VAB_Servicos'],
                               title="Evolução Histórica: Indústria vs Serviços",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00"},
                               markers=True)
        fig_evolucao.update_xaxes(dtick=1)
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('<div class="chart-caption">A linha de Serviços apresenta uma inclinação mais acentuada, indicando mudança no perfil econômico municipal.</div>', unsafe_allow_html=True)

    with col_right:
        fig_pizza = px.pie(df_seg, values='VAB_Pct', names='Segmento', hole=.4, title="Riqueza Industrial por CNAE")
        st.plotly_chart(fig_pizza, use_container_width=True)

elif menu == "Diagnóstico Indústria 4.0":
    st.markdown('<p class="section-title">Maturidade Digital</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_prod = px.bar(df_hist, x='Ano', y='Produtividade', title="Produtividade (R$ / Operário)", color_discrete_sequence=['#1E3A8A'])
        fig_prod.update_xaxes(dtick=1)
        st.plotly_chart(fig_prod, use_container_width=True)
    with c2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=df_seg['Maturidade_Atual'], theta=df_seg['Segmento'], fill='toself', marker=dict(color='#FF8C00')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Nível de Automação por Setor")
        st.plotly_chart(fig_radar, use_container_width=True)

elif menu == "Projeção Futura":
    st.markdown('<p class="section-title">Análise Preditiva de Cenários</p>', unsafe_allow_html=True)
    # ... (restante da lógica de projeção original do seu código)
