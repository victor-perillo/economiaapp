# --- 4. DASHBOARD EXECUTIVO ---
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
        # Dados IPCA Votorantim (Exemplo de série histórica para o cálculo)
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
