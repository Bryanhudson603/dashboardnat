import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Inicializa df como None
df = None
df_filtered = None

# Upload do arquivo CSV
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(uploaded_file, delimiter=';', decimal=",", encoding='ISO-8859-1', parse_dates=['Data Ini'], dayfirst=True)
        
        # Verificar se a coluna "setores" existe no DataFrame
        if "setores" in df.columns:
            # Adicionar filtro para tipo de setores na barra lateral
            setores_options = ["Todos"] + list(df["setores"].unique())  # Adiciona a opção "Todos" ao início da lista

            # Adicionar filtro por data na barra lateral
            if "Data Ini" in df.columns:
                min_date = df["Data Ini"].min().date()  # Convertendo para datetime.date
                max_date = df["Data Ini"].max().date()  # Convertendo para datetime.date
                start_date = st.sidebar.date_input("Data de início", min_value=min_date, max_value=max_date, value=min_date, key="start_date")
                end_date = st.sidebar.date_input("Data de término", min_value=min_date, max_value=max_date, value=max_date, key="end_date")

                # Filtrar os dados por data
                df_filtered = df[(df["Data Ini"].dt.date >= start_date) & (df["Data Ini"].dt.date <= end_date)]

                # Calcular o número total de atendimentos
                total_atendimentos = df_filtered.shape[0]

                # Restante do código para visualização e interação com os dados
            else:
                st.warning("O arquivo não contém uma coluna chamada 'Data Ini'.")
        else:
            st.warning("O arquivo não contém uma coluna chamada 'setores'.")

    except Exception as e:
        st.error(f"Erro ao ler arquivo CSV: {e}")
        st.stop()

# Gráficos
if df_filtered is not None:
    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

    # Definir configurações padrão para os gráficos
    fig_width = 400
    fig_height = 450

    # Filtro para o Gráfico 1: Setores
    selected_setor = st.sidebar.selectbox("Selecione um setor:", ["Todos"] + list(df_filtered["setores"].unique()))

    # Filtro para o Gráfico 3: Atendimento por tipo de produto
    selected_produto = st.sidebar.selectbox("Selecione um produto:", ["Todos"] + list(df_filtered["Plano Principal"].unique()))

    # Filtro para o Gráfico 4: Atendimento por Bairro
    selected_bairro = st.sidebar.selectbox("Selecione um bairro:", ["Todos"] + list(df_filtered["Bairro"].unique()))

    # Filtro para o Gráfico 2: Atendimento por dia
    selected_data = st.sidebar.selectbox("Selecione uma data (Caso queira um dia epecifico no intervalo definido):", ["Todos"] + list(df_filtered["Data Ini"].dt.date.unique()))

    # Filtro para o Gráfico 5: Motivo
    selected_motivo = st.sidebar.selectbox("Selecione um motivo:", ["Todos"] + list(df_filtered["Motivo"].unique()))

    # Filtrar os dados com base nos filtros selecionados
    filtered_data = df_filtered.copy()

    if selected_setor != "Todos":
        filtered_data = filtered_data[filtered_data["setores"] == selected_setor]

    if selected_produto != "Todos":
        filtered_data = filtered_data[filtered_data["Plano Principal"] == selected_produto]

    if selected_bairro != "Todos":
        filtered_data = filtered_data[filtered_data["Bairro"] == selected_bairro]

    if selected_data != "Todos":
        filtered_data = filtered_data[filtered_data["Data Ini"].dt.date == selected_data]

    if selected_motivo != "Todos":
        filtered_data = filtered_data[filtered_data["Motivo"] == selected_motivo]

    # Gráfico 1: Setores
    setores_counts = filtered_data["setores"].value_counts().head(10).reset_index()
    setores_counts.columns = ["setores", "Contagem"]
    fig_setores = px.bar(setores_counts, x="setores", y="Contagem", title="Setor",
                          color="setores")  # Usando a coluna 'Setor' para colorir
    fig_setores.update_layout(title={'x':0.5, 'xanchor': 'center'})
    fig_setores.update_layout(width=fig_width, height=fig_height)
    col1.plotly_chart(fig_setores, use_container_width=True)

    # Gráfico 2: Atendimento por dia
    atendimento_por_dia_counts = filtered_data['Data Ini'].value_counts().reset_index()
    atendimento_por_dia_counts.columns = ["Data Ini", "Total"]
    fig_atendimento_dia_counts = px.bar(atendimento_por_dia_counts, x='Data Ini', y='Total', title='Atendimento por dia',
                                        color="Data Ini")
    fig_atendimento_dia_counts.update_layout(title={'x':0.5, 'xanchor': 'center'})
    fig_atendimento_dia_counts.update_layout(width=fig_width, height=fig_height)
    col2.plotly_chart(fig_atendimento_dia_counts, use_container_width=True)
    
    # Gráfico 3: Atendimento por tipo de produto
    prod_counts = filtered_data["Plano Principal"].value_counts().head(10).reset_index()
    prod_counts.columns = ["Plano Principal", "Contagem"]
    fig_prod = px.pie(prod_counts, values="Contagem", names="Plano Principal", title="Atendimento por plano")
    fig_prod.update_traces(textposition='inside', textinfo='percent+label')
    fig_prod.update_layout(title={'x':0.5, 'xanchor': 'center'})
    fig_prod.update_layout(width=fig_width, height=fig_height)
    col3.plotly_chart(fig_prod, use_container_width=True)

    # Gráfico 4: Atendimento por Bairro
    bairro_counts = filtered_data["Bairro"].value_counts().head(10).reset_index()
    bairro_counts.columns = ["Bairro", "Contagem"]
    fig_bairro = px.bar(bairro_counts, x="Bairro", y="Contagem", title="Atendimento por Bairro",
                      color="Bairro")  # Usando a coluna 'Bairro' para colorir
    fig_bairro.update_layout(title={'x':0.5, 'xanchor': 'center'})
    fig_bairro.update_layout(width=fig_width, height=fig_height)
    col4.plotly_chart(fig_bairro, use_container_width=True)

    # Gráfico 5: Motivo
    motivo_counts = filtered_data["Motivo"].value_counts().head(10).reset_index()
    motivo_counts.columns = ["Motivo", "Contagem"]
    fig_mot = px.bar(motivo_counts, x="Motivo", y="Contagem", title="Motivos",
                     color="Motivo")  # Usando a coluna 'Motivo' para colorir
    fig_mot.update_layout(title={'x':0.5, 'xanchor': 'center'})
    fig_mot.update_layout(width=fig_width, height=fig_height)
    col5.plotly_chart(fig_mot, use_container_width=True)

    # Checkbox para mostrar/ocultar os Top 5
    show_top10 = st.checkbox("Mostrar Top 10")

    if show_top10:
        # Top 10 ao lado dos gráficos
        st.write("**Top 10**")

        top10_setores = setores_counts.head(10).copy()
        top10_setores.index += 1
        top10_produtos = prod_counts.head(10).copy()
        top10_produtos.index += 1
        top10_bairros = bairro_counts.head(10).copy()
        top10_bairros.index += 1
        top10_motivos = motivo_counts.head(10).copy()
        top10_motivos.index += 1

        # "Top 10" lado a lado
        col_top10_1, col_top10_2 = st.columns(2)

        with col_top10_1:
            st.write("Top 10 Setores:")
            st.write(top10_setores)
            st.write("Top 10 Bairros:")
            st.write(top10_bairros)

        with col_top10_2:
            st.write("Top 10 Plano Principal:")
            st.write(top10_produtos)
            st.write("Top 10 Motivos:")
            st.write(top10_motivos)