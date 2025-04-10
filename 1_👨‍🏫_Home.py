import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm, poisson, binom

# Carregar os arquivos CSV
file_ocorrencias = 'indicadoressegurancapublicauf.xlsx'
file_vitimas = "indicadoressegurancapublicamunic.xlsx"
df_ocorrencias = pd.read_excel(file_ocorrencias, engine="openpyxl")  # Lendo o arquivo Excel
df_vitimas = pd.read_excel(file_vitimas, engine="openpyxl")


# Título principal
st.title("📊 Dashboard de Ocorrências Criminais no Brasil")


# Lista de alunos e RMs
dados_autores = [
    {"Nome": "Rafael de Almeida Sigoli", "RM": 554019},
    {"Nome": "Giovanna Franco Gaudino Rodrigues", "RM": 553701},
    {"Nome": "Lucas Bertolassi Iori", "RM": 553183},
    {"Nome": "Enzzo Monteiro Barros", "RM": 552616},
    {"Nome": "Lucas Eduardo Garcia", "RM": 554070},
    {"Nome": "Felipe Santana", "RM": 554259},
    {"Nome": "Enzo Figueiredo Barbeli", "RM": 554272}
]

# Criar DataFrame e exibir como tabela
df_autores = pd.DataFrame(dados_autores)
st.subheader("👨‍💻 Integrantes do Projeto")
st.table(df_autores)

# Introdução ao Dataset
st.header("📁 1. Introdução aos Dados", anchor="introducao-ao-dataset")
st.write("""
🔍 Esta análise utiliza dados extraídos das plataformas **SinespJC** e **Sinesp Integração**, mantidas pelo Governo Federal.  
📌 O **SinespJC** coleta boletins de ocorrência das Polícias Civis desde 2004.  
📌 O **Sinesp Integração**, criado em 2015, unifica diversas fontes para uma visão mais ampla da segurança pública.  
📅 Os dados incluem registros como **homicídios**, **furtos**, **roubos de veículos**, entre outros, e são atualizados periodicamente.
""")


st.markdown("""
## 🧠 Perguntas para Análise

### 📆 Análise Temporal
1. Como os crimes evoluíram ao longo dos anos?  
2. Há uma tendência de aumento ou queda para crimes específicos?  
3. Em quais meses ocorrem mais crimes?

### 🗺️ Análise Geográfica
4. Quais estados têm os maiores e menores índices de criminalidade?  
5. Como os crimes se distribuem pelas regiões do Brasil?

### 🕵️ Análise por Tipo de Crime
6. Qual crime aparece com mais frequência?  
7. Existe variação sazonal em algum tipo de crime?

### 👥 Análise de Vítimas
8. Há diferença no número de vítimas entre homens e mulheres?  
9. Quais crimes mais afetam cada sexo?  
10. Há correlação entre número de ocorrências e número de vítimas?

### 📐 Intervalos de Confiança
11. Qual o intervalo de confiança de 95% para a média de homicídios dos últimos 5 anos?  
12. Qual o intervalo de confiança da proporção de roubos de veículos em relação ao total de crimes?  
13. Existem diferenças significativas entre médias de crimes nas regiões Norte e Sul?

### ⚖️ Testes de Hipótese
14. A média de homicídios em SP é maior do que no RJ?  
15. Há diferenças entre as regiões em relação à média de crimes?  
16. O crime mais comum muda conforme o estado?  
17. Sexo da vítima está relacionado ao tipo de crime?
""")


# Visualização inicial dos dados
st.subheader("👀 Visualização das Primeiras Linhas dos Dados")
st.write("📄 Tabela de Ocorrências:")
st.dataframe(df_ocorrencias.head())

st.write("📄 Tabela de Vítimas:")
st.dataframe(df_vitimas.head())  # Exibir os dados na tela


# Identificação dos tipos de variáveis
st.subheader("Tipos de variáveis no dataset:", anchor="tipos-de-variaveis")
tipo_dados = {
    "UF (Unidade Federativa)": "Qualitativo nominal",
    "Tipo Crime": "Qualitativa Nominal",
    "Ano": "Quantitativo discreto",
    "Mês": "Qualitativo ordinal",
    "Ocorrências": "Quantitativo discreto",
    "Sexo da Vítima": "Qualitativo nominal",
    "Vítimas": "Quantitativo discreto"
}

st.write(pd.DataFrame(tipo_dados.items(), columns=["Coluna", "Tipo de Dado"]))