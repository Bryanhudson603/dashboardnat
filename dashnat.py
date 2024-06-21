import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

# Função para calcular os dados do dashboard de Atendimento
def calcular_dados_atendimento(df):
    # Verificar se a coluna "setores" existe no DataFrame
    # Converter a coluna "Data Ini" para objetos de data
    df['Data Ini'] = pd.to_datetime(df['Data Ini'], dayfirst=True)

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

                # Checkbox para mostrar/ocultar os Top 10
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

# Função para calcular os dados do dashboard de Faturas
def calcular_dados_faturas(df):
    required_columns = ["Quant Faturas", "Divida en Aberto", "Plano PPal", "Bairro", "Cidade"]
    if all(column in df.columns for column in required_columns):
        df["Divida en Aberto"] = pd.to_numeric(df["Divida en Aberto"].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        df_filtered = df.copy()

        fatura_filter = st.sidebar.multiselect("Quantidade de Faturas", options=df_filtered["Quant Faturas"].unique())
        plano_filter = st.sidebar.multiselect("Planos", options=df_filtered["Plano PPal"].unique())
        cidade_filter = st.sidebar.multiselect("Cidades", options=df_filtered["Cidade"].unique())

        if fatura_filter:
            df_filtered = df_filtered[df_filtered["Quant Faturas"].isin(fatura_filter)]
        if plano_filter:
            df_filtered = df_filtered[df_filtered["Plano PPal"].isin(plano_filter)]
        if cidade_filter:
            df_filtered = df_filtered[df_filtered["Cidade"].isin(cidade_filter)]

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        fig_width = 400
        fig_height = 450

        # Gráfico 1: Quantidade de Faturas
        faturas_counts = df_filtered["Quant Faturas"].value_counts().head(10).reset_index()
        faturas_counts.columns = ["Quant Faturas", "Contagem"]
        fig_faturas = px.bar(faturas_counts, x="Quant Faturas", y="Contagem", title="Faturas em aberto (Qtd)",
                             color="Quant Faturas")
        fig_faturas.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_faturas.update_layout(width=fig_width, height=fig_height)
        col1.plotly_chart(fig_faturas, use_container_width=True)

        # Gráfico 2: Atendimento por Plano
        plano_counts = df_filtered["Plano PPal"].value_counts().head(10).reset_index()
        plano_counts.columns = ["Plano PPal", "Contagem"]
        fig_plano = px.pie(plano_counts, values="Contagem", names="Plano PPal", title="Atendimento por Combo (%)")
        fig_plano.update_traces(textposition='inside', textinfo='percent+label')
        fig_plano.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_plano.update_layout(width=fig_width, height=fig_height)
        col2.plotly_chart(fig_plano, use_container_width=True)

        # Gráfico 3: Soma das Faturas
        soma_faturas = df_filtered.groupby("Quant Faturas").agg({"Divida en Aberto": "sum"}).reset_index()
        soma_faturas.columns = ["Quant Faturas", "Soma da Divida em Aberto"]
        fig_soma_faturas = px.bar(soma_faturas, x="Quant Faturas", y="Soma da Divida em Aberto", title="Somatório dos Valores (R$)",
                                  color="Quant Faturas")
        fig_soma_faturas.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_soma_faturas.update_layout(width=fig_width, height=fig_height)
        fig_soma_faturas.update_traces(textposition='outside')
        col3.plotly_chart(fig_soma_faturas, use_container_width=True)

        # Gráfico 4: Cidades com Dívidas
        cidade_counts = df_filtered["Cidade"].value_counts().head(10).reset_index()
        cidade_counts.columns = ["Cidade", "Contagem"]
        fig_cidade = px.bar(cidade_counts, x="Cidade", y="Contagem", title="Inadimplentes por Cidade",
                            color="Cidade")
        fig_cidade.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_cidade.update_layout(width=fig_width, height=fig_height)
        col4.plotly_chart(fig_cidade, use_container_width=True)

        # Checkbox para mostrar/ocultar os Top 10
        show_top10 = st.checkbox("Mostrar Top 10")

        if show_top10:
            st.write("**Top 10**")

            top10_faturas = faturas_counts.head(10).copy()
            top10_soma_faturas = soma_faturas.head(10).copy()

            # Junção dos Top 10 Quantidade de Faturas e Soma das Faturas
            top10_combined = pd.merge(top10_faturas, top10_soma_faturas, on="Quant Faturas", how="outer")
            top10_combined.index += 1

            top10_planos = plano_counts.head(10).copy()
            top10_planos.index += 1
            top10_cidades = cidade_counts.head(10).copy()
            top10_cidades.index += 1

            col_top10_1, col_top10_2 = st.columns(2)

            with col_top10_1:
                st.write("Top 10 Quantidade e Soma das Faturas:")
                st.write(top10_combined)

            with col_top10_2:
                st.write("Top 10 Planos:")
                st.write(top10_planos)
                st.write("Top 10 Cidades:")
                st.write(top10_cidades)

    else:
        st.warning("O arquivo não contém todas as colunas necessárias.")

# Função para calcular os dados de inadimplentes
def calcular_dados_inadimplentes(df):
    required_columns = ["Id Cli", "Plano", "Cnx Status", "Valor", "Produto", "Cidade", "Bairro"]
    if all(column in df.columns for column in required_columns):
        # Eliminar duplicatas considerando apenas Id Cli, Plano e Cnx Status
        df_filtered = df.drop_duplicates(subset=["Id Cli", "Plano", "Cnx Status"])

        # Adicionar filtros
        plano_filter = st.sidebar.multiselect("Planos", options=df_filtered["Plano"].unique())
        status_filter = st.sidebar.multiselect("Status de Conexão", options=df_filtered["Cnx Status"].unique())

        if plano_filter:
            df_filtered = df_filtered[df_filtered["Plano"].isin(plano_filter)]
        if status_filter:
            df_filtered = df_filtered[df_filtered["Cnx Status"].isin(status_filter)]
    else:
        st.warning("O arquivo não contém todas as colunas necessárias.")
        
    # Gráficos
    if df_filtered is not None:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        col7, col8 = st.columns(2)

        # Definir configurações padrão para os gráficos
        fig_width = 400
        fig_height = 450

        # Gráfico 1: Quantidade de Clientes por Plano
        plano_counts = df_filtered.groupby("Plano")["Id Cli"].nunique().reset_index()
        plano_counts.columns = ["Plano", "Quantidade de Clientes"]
        top_10_planos = plano_counts.nlargest(10, "Quantidade de Clientes")  # Selecionar os 10 principais planos
        fig_plano = px.bar(top_10_planos, x="Plano", y="Quantidade de Clientes", title="Quantidade de Clientes por Plano (Top 10)",
                           color="Plano")
        fig_plano.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_plano.update_layout(width=fig_width, height=fig_height)
        col1.plotly_chart(fig_plano, use_container_width=True)
        
        # Gráfico 2: Percentual de Clientes por Status de Conexão
        status_counts = df_filtered["Cnx Status"].value_counts(normalize=True).reset_index()
        status_counts.columns = ["Cnx Status", "Percentual"]
        fig_status = px.pie(status_counts, values="Percentual", names="Cnx Status", title="Percentual de Clientes por Status de Conexão")
        fig_status.update_traces(textposition='inside', textinfo='percent+label')
        fig_status.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_status.update_layout(width=fig_width, height=fig_height)
        col2.plotly_chart(fig_status, use_container_width=True)

        # Gráfico 3: Percentual de Clientes Inadimplentes e Suspensos por Plano (mesma ordem do Gráfico 1)
        total_clientes_por_plano = df_filtered.groupby("Plano")["Id Cli"].nunique().reset_index()
        total_clientes_por_plano.columns = ["Plano", "Total de Clientes"]
        
        inadimplente_suspenso_df = df_filtered[df_filtered["Cnx Status"].isin(["Inadimplente", "Suspenso"])]
        inadimplente_suspenso_counts = inadimplente_suspenso_df.groupby("Plano")["Id Cli"].nunique().reset_index()
        inadimplente_suspenso_counts.columns = ["Plano", "Quantidade de Clientes Inadimplentes/Suspensos"]
        
        merged_df = pd.merge(inadimplente_suspenso_counts, total_clientes_por_plano, on="Plano")
        merged_df["Percentual Inadimplentes/Suspensos"] = (merged_df["Quantidade de Clientes Inadimplentes/Suspensos"] / merged_df["Total de Clientes"]) * 100
        
        # Ordenar pelo total de clientes para manter a mesma ordem do gráfico 1
        merged_df = merged_df.set_index("Plano").reindex(top_10_planos["Plano"]).reset_index()
        
        fig_inadimplente_suspenso = px.bar(merged_df, x="Plano", y="Percentual Inadimplentes/Suspensos", 
                                           title="Percentual de Clientes Inadimplentes e Suspensos por Plano (Top 10)",
                                           color="Plano")
        fig_inadimplente_suspenso.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_inadimplente_suspenso.update_layout(width=fig_width, height=fig_height)
        col3.plotly_chart(fig_inadimplente_suspenso, use_container_width=True)

    # Gráfico 4: Soma dos Valores de Clientes Inadimplentes e Suspensos por Status (sem remoção de duplicatas e sem limitar os planos)
    if "Valor" in df.columns:
        # Corrigir valores na coluna "Valor"
        df["Valor"] = df["Valor"].astype(str).str.replace('[^0-9,]', '', regex=True).str.replace(',', '.')
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0)

        # Filtrar apenas os clientes inadimplentes e suspensos
        inadimplente_suspenso_df = df[df["Cnx Status"].isin(["Inadimplente", "Suspenso"])]

        # Calcular a soma dos valores por status de conexão
        soma_inadimplente = inadimplente_suspenso_df[inadimplente_suspenso_df["Cnx Status"] == "Inadimplente"]["Valor"].sum()
        soma_suspenso = inadimplente_suspenso_df[inadimplente_suspenso_df["Cnx Status"] == "Suspenso"]["Valor"].sum()

        valor_soma = pd.DataFrame({"Cnx Status": ["Inadimplente", "Suspenso"],
                                   "Soma dos Valores": [soma_inadimplente, soma_suspenso]})

        # Formatar os valores como moeda
        valor_soma["Soma dos Valores"] = valor_soma["Soma dos Valores"].apply(lambda x: f'R${x:,.2f}')
        
        # Gerar o gráfico
        fig_valor_soma = px.bar(valor_soma, x="Cnx Status", y="Soma dos Valores", title="Soma dos Valores de Clientes Inadimplentes e Suspensos",
                                color="Cnx Status", text="Soma dos Valores")
        fig_valor_soma.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_valor_soma.update_layout(width=fig_width, height=fig_height)
        col4.plotly_chart(fig_valor_soma, use_container_width=True)
    else:
        col4.warning("A coluna 'Valor' não está presente no arquivo CSV.")

    # Gráfico 5: Valor Total por Plano (Top 10)
    if "Valor" in df.columns:
        valor_por_plano = df.groupby("Plano")["Valor"].sum().reset_index()
        top_10_valor_por_plano = valor_por_plano.nlargest(10, "Valor")
        top_10_valor_por_plano = top_10_valor_por_plano.set_index("Plano").reindex(top_10_planos["Plano"]).reset_index() # Mantém a mesma ordem dos top 10 planos
        fig_valor_plano = px.bar(top_10_valor_por_plano, x="Plano", y="Valor", title="Valor Total por Plano (Top 10)",
                                 color="Plano")
        fig_valor_plano.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_valor_plano.update_layout(width=fig_width, height=fig_height)
        col5.plotly_chart(fig_valor_plano, use_container_width=True)
    else:
        st.warning("A coluna 'Valor' não está presente no arquivo CSV.")

    # Gráfico 6: Cidades com Inadimplentes e Suspensos
    if df_filtered is not None:
        # Aplicar filtros
        if plano_filter:
            df_filtered_6 = df_filtered[df_filtered["Plano"].isin(plano_filter)]
        else:
            df_filtered_6 = df_filtered
        if status_filter:
            df_filtered_6 = df_filtered_6[df_filtered_6["Cnx Status"].isin(status_filter)]

        # Remover duplicatas considerando apenas o ID do cliente
        df_filtered_6 = df_filtered_6.drop_duplicates(subset=["Id Cli"])

        # Contar o número de inadimplentes e suspensos por cidade
        inadimplente_suspenso_cidades = df_filtered_6[df_filtered_6["Cnx Status"].isin(["Inadimplente", "Suspenso"])]
        cidade_counts = inadimplente_suspenso_cidades["Cidade"].value_counts().reset_index()
        cidade_counts.columns = ["Cidade", "Quantidade"]

        # Criar o gráfico de barras
        fig_cidades = px.bar(cidade_counts, x="Cidade", y="Quantidade", title="Cidades com Inadimplentes e Suspensos",
                             color="Cidade")
        fig_cidades.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        fig_cidades.update_layout(width=fig_width, height=fig_height)
        col6.plotly_chart(fig_cidades, use_container_width=True)
    
    # Gráfico 7: Bairros com Inadimplentes e Suspensos por Cidade
    if df_filtered is not None:
        # Definir o filtro da cidade para selecionar todas as cidades por padrão
        city_filter = st.sidebar.selectbox("Selecione a Cidade", options=['Todas as Cidades'] + list(df_filtered["Cidade"].unique()))

        if city_filter != 'Todas as Cidades':
            city_filtered_df = df_filtered[df_filtered["Cidade"] == city_filter]
            # Aplicar filtros
            if plano_filter:
                df_filtered_7 = city_filtered_df[city_filtered_df["Plano"].isin(plano_filter)]
            else:
                df_filtered_7 = city_filtered_df
            if status_filter:
                df_filtered_7 = df_filtered_7[df_filtered_7["Cnx Status"].isin(status_filter)]

            # Filtrar apenas os clientes inadimplentes e suspensos
            inadimplente_suspenso_df = df_filtered_7[df_filtered_7["Cnx Status"].isin(["Inadimplente", "Suspenso"])]

            # Contar o número de clientes inadimplentes e suspensos em cada bairro
            bairro_counts = inadimplente_suspenso_df.groupby("Bairro")["Id Cli"].nunique().reset_index()
            bairro_counts.columns = ["Bairro", "Número de Clientes Inadimplentes/Suspensos"]

            # Ordenar os bairros pelo número de clientes inadimplentes e suspensos
            bairro_counts = bairro_counts.sort_values(by="Número de Clientes Inadimplentes/Suspensos", ascending=False)

            # Criar o gráfico de barras
            fig_bairro = px.bar(bairro_counts, x="Bairro", y="Número de Clientes Inadimplentes/Suspensos",
                                title=f"Número de Clientes Inadimplentes e Suspensos por Bairro em {city_filter}",
                                color="Bairro")
            fig_bairro.update_layout(title={'x': 0.5, 'xanchor': 'center'})
            fig_bairro.update_layout(width=fig_width, height=fig_height)
            col7.plotly_chart(fig_bairro, use_container_width=True)

# Função para calcular e exibir a arrecadação por plano


def calcular_arrecadacao_por_plano(df):
    # Verificar se todas as colunas necessárias estão presentes
    required_columns = ["Plano", "Cnx Status", "Valor", "Id Cli", "Cidade"]
    if all(column in df.columns for column in required_columns):
        # Adicionar um filtro de cidade
        cidades = df["Cidade"].unique()
        cidade_selecionada = st.sidebar.selectbox("Selecione a Cidade", options=cidades)
        
        # Filtrar os dados pela cidade selecionada
        df = df[df["Cidade"] == cidade_selecionada]

        # Filtrar os clientes com status conectado
        df_conectados = df[df["Cnx Status"] == "Conectado"]
        
        # Remover caracteres não numéricos e converter para float
        df_conectados["Valor"] = pd.to_numeric(df_conectados["Valor"].str.replace(',', '.'), errors="coerce")
        
        # Substituir valores nulos por zero
        df_conectados["Valor"].fillna(0, inplace=True)
        
        # Inicializar um dicionário para armazenar o valor total por plano
        total_por_plano = {}
        
        # Calcular o valor total por plano
        for index, row in df_conectados.iterrows():
            plano = row["Plano"]
            valor = row["Valor"]
            if plano in total_por_plano:
                total_por_plano[plano] += valor
            else:
                total_por_plano[plano] = valor
        
        # Converter o dicionário em um DataFrame
        df_arrecadacao = pd.DataFrame(list(total_por_plano.items()), columns=["Plano", "Valor Total"])
        
        # Calcular a quantidade de clientes conectados por plano
        quantidade_clientes = df_conectados.groupby("Plano")["Id Cli"].nunique().reset_index()
        quantidade_clientes.columns = ["Plano", "Quantidade de Clientes Conectados"]
        
        # Mesclar os dois dataframes
        df_arrecadacao = pd.merge(df_arrecadacao, quantidade_clientes, on="Plano")
        
        # Calcular o valor médio do plano por cliente
        df_arrecadacao["Valor Médio do Plano"] = df_arrecadacao["Valor Total"] / df_arrecadacao["Quantidade de Clientes Conectados"]
        
        # Reordenar as colunas
        df_arrecadacao = df_arrecadacao[["Plano", "Quantidade de Clientes Conectados", "Valor Médio do Plano", "Valor Total"]]
        
        # Ordenar os planos em ordem numérica
        df_arrecadacao["Plano_Numérico"] = df_arrecadacao["Plano"].str.extract('(\d+)').astype(int)
        df_arrecadacao = df_arrecadacao.sort_values(by="Plano_Numérico")
        df_arrecadacao = df_arrecadacao.drop(columns=["Plano_Numérico"])
        
        # Calcular a soma de todos os valores da coluna "Valor Total"
        soma_valor_total = df_arrecadacao["Valor Total"].sum()
        
        # Formatando os valores como moeda
        df_arrecadacao["Valor Total"] = df_arrecadacao["Valor Total"].apply(lambda x: f"R${x:,.2f}")
        df_arrecadacao["Valor Médio do Plano"] = df_arrecadacao["Valor Médio do Plano"].apply(lambda x: f"R${x:,.2f}")
        
        # Mostrar a tabela de arrecadação
        st.write(f"### Arrecadação por Plano - {cidade_selecionada}")
        st.write(df_arrecadacao)
        
        # Mostrar a soma total
        st.write(f"### Soma Total: R${soma_valor_total:,.2f}")
    else:
        st.warning("O arquivo não contém todas as colunas necessárias.")

# Exemplo de chamada da função (df deve ser definido anteriormente com os dados adequados)
# calcular_arrecadacao_por_plano(df)

# Menu de seleção do dashboard
menu = st.sidebar.selectbox("Selecione o Dashboard", ["Clientes Planos e Produtos", "Faturas em Aberto", "Atendimento", "Cliente - Arrecadação por Plano"])

# Upload do arquivo CSV
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=';', encoding='ISO-8859-1')

    if menu == "Clientes Planos e Produtos":
        calcular_dados_inadimplentes(df)
    elif menu == "Faturas em Aberto":
        calcular_dados_faturas(df)
    elif menu == "Atendimento":
        calcular_dados_atendimento(df)
    elif menu == "Cliente - Arrecadação por Plano":
        calcular_arrecadacao_por_plano(df)
