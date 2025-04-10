import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm, poisson, binom
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import folium 
import geopandas as gpd
from streamlit_folium import folium_static
import plotly.express as px


pages = st.sidebar.selectbox("Análise Exploratória de Crimes", ['Análise Exploratória de Crimes',
    "Análise Temporal",
    "Análise Geográfica [EM TESTE]",
    "Correlações",
    "Distribuição de Poisson [EM ANDAMENTO]",
    "Distribuição Normal [EM ANDAMENTO]",
])

def load_data(file_name):
        try:
            df = pd.read_excel(file_name)
            return df
        except FileNotFoundError:
            st.error(f"Erro: Arquivo '{file_name}' não encontrado.")
        except KeyError as e:
            st.error(f"Erro: Coluna '{e}' não encontrada no DataFrame. Verifique o nome da coluna.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")

    # Função para calcular medidas de tendência central
def calculate_central_tendency(df):
    results = {}
    for crime_type in df['Tipo Crime'].unique():
        crime_data = df[df['Tipo Crime'] == crime_type]
        numeric_cols = [col for col in crime_data.columns if pd.api.types.is_numeric_dtype(crime_data[col])]
        if not numeric_cols:
            results[crime_type] = "Nenhuma coluna numérica encontrada."
            continue
        results[crime_type] = {}
        for col in numeric_cols:
            try:
                mean_val = crime_data[col].mean()
                median_val = crime_data[col].median()
                mode_val = crime_data[col].mode().iloc[0] if not crime_data[col].mode().empty else 'N/A'
                std_dev = crime_data[col].std()
                results[crime_type][col] = {'Mean': mean_val, 'Median': median_val, 'Mode': mode_val, 'Std Dev': std_dev}
            except Exception as e:
                results[crime_type][col] = f"Erro ao calcular estatísticas: {e}"
    return results

def generate_analysis(stats):
    analysis = ""
    for col, values in stats.items():
        if col.lower() == 'ocorrências':  # Focar apenas na análise das ocorrências
            mean_val = values['Mean']
            median_val = values['Median']
            std_dev = values['Std Dev']
            if mean_val > median_val:
                analysis += "A média é maior que a mediana, indicando uma possível assimetria positiva (cauda à direita) na distribuição dos dados.\n"
            else:
                analysis += "A média é menor ou igual à mediana, indicando uma possível assimetria negativa (cauda à esquerda) ou simetria na distribuição dos dados.\n"
            analysis += f"O desvio padrão indica a dispersão dos dados em relação à média. Um valor alto de desvio padrão ({std_dev}) indica maior variabilidade nos dados, enquanto um valor baixo indica menor variabilidade.\n"
    return analysis
    
file_name = "indicadoressegurancapublicauf.xlsx"
st.title("Análise Exploratória dos Dados de Crimes.")
df = pd.read_excel(file_name)
if st.button("Expandir Dados"):
    
    st.write("Dados carregados com sucesso:")
    st.dataframe(df)   
else:
    st.write("Clique no botão acima para expandir e visualizar os dados.")
try:
    
    columns_to_display = [
        "UF", 
        "Tipo Crime", 
        "Ano",
        "Mês",
        "Ocorrências"
    ]
   
    df_filtered = df[columns_to_display]
except FileNotFoundError:
    st.error(f"Arquivo '{file_name}' não encontrado. Certifique-se de que está no mesmo diretório do código.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
    

if pages == "Análise Exploratória de Crimes":
    
    # Carregar os dados
    file_name = 'indicadoressegurancapublicauf.xlsx'
    df = load_data(file_name)

    if df is not None:
        # Título da aplicação
        st.title('Análise de Indicadores de Segurança Pública')

        # Calcular e exibir medidas de tendência central
        st.subheader('Medidas de Tendência Central por Tipo de Crime')
        central_tendency = calculate_central_tendency(df)

        # Criar um seletor para o tipo de crime
        crime_types = list(central_tendency.keys())
        selected_crime = st.selectbox('Selecione o tipo de crime', crime_types, key='crime_selectbox')

        if selected_crime in central_tendency:
            stats = central_tendency[selected_crime]
            st.markdown(f"### {selected_crime}")
            if isinstance(stats, str):
                st.write(stats)
            else:
                crime_df = pd.DataFrame(stats).T
                crime_df.columns = ['Média', 'Mediana', 'Moda', 'Desvio Padrão']
                st.table(crime_df)
                analysis = generate_analysis(stats)
                st.markdown(f"#### Análise dos Dados para {selected_crime}")
                st.text(analysis)

        # Rodapé
        st.markdown('---')
        st.write('Aplicação criada com Streamlit')
        
elif pages == "Análise Temporal":
    # Função para plotar dois crimes comparados no mesmo gráfico
    def plot_compare_crimes(df, crime1, crime2, estado):
        plt.figure(figsize=(12, 6))
        for crime_type in [crime1, crime2]:
            filtered_df = df[(df['Tipo Crime'] == crime_type) & (df['UF'] == estado)]
            if 'Ano' in filtered_df.columns:
                crime_data = filtered_df.groupby('Ano')['Ocorrências'].sum().reset_index()
                plt.plot(crime_data['Ano'], crime_data['Ocorrências'], marker='o', label=crime_type)
            else:
                st.error("A coluna 'Ano' não foi encontrada no DataFrame.")
        plt.title(f'Comparação Temporal: {crime1} vs {crime2} em {estado}')
        plt.xlabel('Ano')
        plt.ylabel('Ocorrências')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    # Carregar os dados
    file_name = 'indicadoressegurancapublicauf.xlsx'
    df = load_data(file_name)

    if df is not None:
        st.title('Análise Temporal dos Crimes')

        # Filtros
        st.subheader('Selecione o estado e dois tipos de crime para comparação')
        estados = sorted(df['UF'].unique())
        crime_types = sorted(df['Tipo Crime'].unique())

        selected_estado = st.selectbox('Selecione o estado (UF)', estados)
        selected_crime1 = st.selectbox('Selecione o 1º tipo de crime', crime_types, key='crime1')
        selected_crime2 = st.selectbox('Selecione o 2º tipo de crime', crime_types, key='crime2')

        # Evitar que o mesmo crime seja selecionado duas vezes
        if selected_crime1 == selected_crime2:
            st.warning("Por favor, selecione dois tipos de crime diferentes para comparação.")
        else:
            # Mostrar gráfico comparativo
            st.subheader(f'Comparação entre {selected_crime1} e {selected_crime2} em {selected_estado}')
            plot_compare_crimes(df, selected_crime1, selected_crime2, selected_estado)




elif pages == "Análise Geográfica":
    
#     def load_brazil_map():
#         try:
#             gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#             brazil = gdf[gdf.name == "Brazil"]
#             return brazil
#         except Exception as e:
#             st.error(f"Ocorreu um erro ao carregar o mapa do Brasil: {e}")

# # Função para criar gráfico de dispersão geral
#     def plot_general_scatter(df, brazil):
#         uf_data = df.groupby('UF')['Ocorrências'].sum().reset_index()
#         uf_data = uf_data.merge(brazil, left_on='UF', right_on='adm1_code')
#         m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
#         for _, row in uf_data.iterrows():
#             folium.CircleMarker(
#                 location=[row['latitude'], row['longitude']],
#                 radius=row['Ocorrências'] / 1000,
#                 color='blue',
#                 fill=True,
#                 fill_color='blue'
#             ).add_to(m)
#         folium_static(m)

#     # Função para criar mapa de calor por tipo de crime
#     def plot_heatmap(df, crime_type, brazil):
#         crime_data = df[df['Tipo Crime'] == crime_type]
#         uf_data = crime_data.groupby('UF')['Ocorrências'].sum().reset_index()
#         uf_data = uf_data.merge(brazil, left_on='UF', right_on='adm1_code')
#         m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
#         folium.Choropleth(
#             geo_data=uf_data,
#             name='choropleth',
#             data=uf_data,
#             columns=['UF', 'Ocorrências'],
#             key_on='feature.properties.adm1_code',
#             fill_color='YlOrRd',
#             fill_opacity=0.7,
#             line_opacity=0.2,
#             legend_name='Ocorrências'
#         ).add_to(m)
#         folium_static(m)

#     # Carregar os dados
#     file_name = 'indicadoressegurancapublicauf.xlsx'
#     df = load_data(file_name)

#     if df is not None:
#         # Carregar o mapa do Brasil
#         brazil = load_brazil_map()

#         if brazil is not None:
#             # Configurar a barra lateral
#             st.sidebar.title('Menu')
#             page = st.sidebar.selectbox('Selecione a página', ['Análise Geográfica Geral', 'Mapa de Calor por Crime'])

#             if page == 'Análise Geográfica Geral':
#                 # Título da aplicação
#                 st.title('Análise Geográfica Geral dos Crimes')

#                 # Plotar gráfico de dispersão geral
#                 plot_general_scatter(df, brazil)

#             elif page == 'Mapa de Calor por Crime':
#                 # Título da aplicação
#                 st.title('Mapa de Calor por Crime')

#                 # Criar um seletor para o tipo de crime
#                 crime_types = df['Tipo Crime'].unique()
#                 selected_crime = st.selectbox('Selecione o tipo de crime', crime_types, key='heatmap_selectbox')

#                 # Plotar mapa de calor para o tipo de crime selecionado
#                 plot_heatmap(df, selected_crime, brazil)

#             # Rodapé
#             st.sidebar.markdown('---')
#             st.sidebar.write('Aplicação criada com Streamlit')


    
    # 
    # def load_data(file_name):
    #     try:
    #         df = pd.read_excel(file_name, engine='openpyxl')
    #         return df
    #     except Exception as e:
    #         st.error(f"Ocorreu um erro ao carregar os dados: {e}")
    #         return None

    # # Função para criar gráfico de dispersão geral com diferentes crimes
    # def plot_general_scatter(df):
    #     fig = px.scatter_geo(df, locations="UF", color="Tipo Crime", size="Ocorrências", hover_name="UF",
    #                         projection="natural earth", title="Análise Geográfica Geral dos Crimes")
    #     st.plotly_chart(fig)

    # # Função para criar mapa de calor por tipo de crime
    # def plot_heatmap(df, crime_type):
    #     crime_data = df[df['Tipo Crime'] == crime_type]
    #     uf_data = crime_data.groupby('UF')['Ocorrências'].sum().reset_index()
    #     fig = px.choropleth(uf_data, locations="UF", color="Ocorrências",
    #                         hover_name="UF", projection="natural earth",
    #                         title=f"Mapa de Calor por Crime: {crime_type}")
    #     st.plotly_chart(fig)

    # # Carregar os dados
    # file_name = 'indicadoressegurancapublicauf.xlsx'
    # df = load_data(file_name)

    # if df is not None:
    #     # Título da aplicação
    #     st.title('Análise de Crimes no Brasil')

    #     # Plotar gráfico de dispersão geral com diferentes crimes
    #     plot_general_scatter(df)

    #     # Criar um seletor para o tipo de crime
    #     crime_types = df['Tipo Crime'].unique()
    #     selected_crime = st.selectbox('Selecione o tipo de crime para o mapa de calor', crime_types, key='heatmap_selectbox')

    #     # Plotar mapa de calor para o tipo de crime selecionado
    #     plot_heatmap(df, selected_crime)
        
    def load_data(file_name):
        try:
            df = pd.read_excel(file_name, engine='openpyxl')
            return df
        except Exception as e:
            st.error(f"Ocorreu um erro ao carregar os dados: {e}")
            return None

    # Lista de correspondência entre nomes dos estados e suas siglas
    state_to_code = {
        "Acre": "AC",
        "Alagoas": "AL",
        "Amapá": "AP",
        "Amazonas": "AM",
        "Bahia": "BA",
        "Ceará": "CE",
        "Distrito Federal": "DF",
        "Espírito Santo": "ES",
        "Goiás": "GO",
        "Maranhão": "MA",
        "Mato Grosso": "MT",
        "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG",
        "Pará": "PA",
        "Paraíba": "PB",
        "Paraná": "PR",
        "Pernambuco": "PE",
        "Piauí": "PI",
        "Rio de Janeiro": "RJ",
        "Rio Grande do Norte": "RN",
        "Rio Grande do Sul": "RS",
        "Rondônia": "RO",
        "Roraima": "RR",
        "Santa Catarina": "SC",
        "São Paulo": "SP",
        "Sergipe": "SE",
        "Tocantins": "TO"
    }

    # Função para criar gráfico de dispersão geral com diferentes crimes
    def plot_general_scatter(df):
        df['UF_code'] = df['UF'].map(state_to_code)
        fig = px.scatter_geo(df, locations="UF_code", color="Tipo Crime", size="Ocorrências", hover_name="UF",
                            projection="natural earth", title="Análise Geográfica Geral dos Crimes")
        st.plotly_chart(fig)

    # Função para criar mapa de calor por tipo de crime
    def plot_heatmap(df, crime_type):
        crime_data = df[df['Tipo Crime'] == crime_type]
        uf_data = crime_data.groupby('UF')['Ocorrências'].sum().reset_index()
        uf_data['UF_code'] = uf_data['UF'].map(state_to_code)
        fig = px.choropleth(uf_data, locations="UF_code", color="Ocorrências",
                            hover_name="UF", projection="natural earth",
                            title=f"Mapa de Calor por Crime: {crime_type}")
        st.plotly_chart(fig)

    # Carregar os dados
    file_name = 'indicadoressegurancapublicauf.xlsx'
    df = load_data(file_name)

    if df is not None:
        # Título da aplicação
        st.title('Análise de Crimes no Brasil')

        # Plotar gráfico de dispersão geral com diferentes crimes
        plot_general_scatter(df)

        # Criar um seletor para o tipo de crime
        crime_types = df['Tipo Crime'].unique()
        selected_crime = st.selectbox('Selecione o tipo de crime para o mapa de calor', crime_types, key='heatmap_selectbox')

        # Plotar mapa de calor para o tipo de crime selecionado
        plot_heatmap(df, selected_crime)
        
    