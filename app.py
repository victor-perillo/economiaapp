# --- 1. ATUALIZAÇÃO DOS DADOS (Substitua sua função load_data por esta) ---
@st.cache_data
def load_data():
    df_seg = pd.DataFrame({
        'Segmento': ["Minerais Não Metálicos", "Metalurgia", "Papel e Celulose", "Química/Plásticos", "Alimentos", "Outros"],
        'VAB_Pct': [48, 18, 15, 10, 6, 3],
        'Dificuldade_40': [65, 55, 40, 50, 80, 45], 
        'Maturidade_Atual': [2.8, 3.2, 3.5, 2.9, 1.8, 2.4] 
    })
    
    # Dados extraídos do seu anexo e projeções baseadas no PIB
    df_hist = pd.DataFrame({
        'Ano': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'Produtividade': [185, 198, 210, 225, 242, 268, 285, 302], 
        'VAB_Industria': [732.1, 785.4, 810.2, 932.4, 1020.0, 1110.0, 1220.0, 1350.0],
        'VAB_Servicos': [1480.0, 1590.0, 1620.0, 1897.8, 2120.0, 2350.0, 2610.0, 2900.0],
        'PIB': [3056.0, 3284.0, 3391.0, 3922.0, 4410.0, 4850.0, 5335.0, 5870.0]
    })
    return df_seg, df_hist

df_seg, df_hist = load_data()

# --- 2. FUNÇÃO DE FORMATAÇÃO Mi/Bi ---
def formatar_valor(valor):
    if valor >= 1000:
        return f"R$ {valor/1000:.2f} Bi"
    return f"R$ {valor:.1f} Mi"

# --- 3. AJUSTE NO DASHBOARD EXECUTIVO (Substitua este menu no seu código) ---
elif menu == "Dashboard Executivo":
    st.markdown('<p class="section-title">Panorama Macro de Votorantim</p>', unsafe_allow_html=True)
    
    # Cards Dinâmicos
    c1, c2, c3, c4 = st.columns(4)
    
    # Lógica para Delta do PIB
    if ano_selecionado != "Todos":
        dados_atuais = df_hist[df_hist['Ano'] == int(ano_selecionado)].iloc[0]
        idx = df_hist[df_hist['Ano'] == int(ano_selecionado)].index[0]
        pib_val = dados_atuais['PIB']
        vab_i = dados_atuais['VAB_Industria']
        vab_s = dados_atuais['VAB_Servicos']
        prod = dados_atuais['Produtividade']
        
        # Delta PIB
        delta_pib = None
        if idx > 0:
            pib_ant = df_hist.iloc[idx-1]['PIB']
            delta_pib = f"{((pib_val/pib_ant)-1)*100:.1f}%"
    else:
        # Se selecionar "Todos", mostra o último ano da série
        dados_ult = df_hist.iloc[-1]
        pib_val, vab_i, vab_s, prod = dados_ult['PIB'], dados_ult['VAB_Industria'], dados_ult['VAB_Servicos'], dados_ult['Produtividade']
        delta_pib = "Série Histórica"

    with c1:
        st.metric("PIB Municipal", formatar_valor(pib_val), delta=delta_pib)
    with c2:
        st.metric("VAB Indústria", formatar_valor(vab_i))
    with c3:
        st.metric("VAB Serviços", formatar_valor(vab_s))
    with c4:
        st.metric("Produtividade", f"R$ {prod}k")

    # Gráficos
    col_left, col_right = st.columns([0.6, 0.4])
    with col_left:
        fig_evolucao = px.line(df_hist, x='Ano', y=['VAB_Industria', 'VAB_Servicos', 'PIB'],
                               title="Evolução Econômica: PIB vs Setores",
                               color_discrete_map={"VAB_Industria": "#1E3A8A", "VAB_Servicos": "#FF8C00", "PIB": "#2b8a3e"},
                               markers=True)
        st.plotly_chart(fig_evolucao, use_container_width=True)

    with col_right:
        # Gráfico de pizza baseado no VAB do ano selecionado ou último ano
        vab_total_ano = vab_i + vab_s
        fig_dist = px.pie(values=[vab_i, vab_s], names=['Indústria', 'Serviços'], 
                          hole=.4, title=f"Composição VAB ({ano_selecionado if ano_selecionado != 'Todos' else '2025'})",
                          color_discrete_sequence=["#1E3A8A", "#FF8C00"])
        st.plotly_chart(fig_dist, use_container_width=True)
