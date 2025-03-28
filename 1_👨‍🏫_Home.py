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


# Streamlit - Interface do Dashboard
st.title("Análise de ocorrencias criminais")


# Apresentação do Dataset
st.header("1. Introdução ao Dataset", anchor="introducao-ao-dataset")
st.write("Os dados utilizados nesta análise foram extraídos das plataformas SinespJC e Sinesp Integração, desenvolvidas pelo governo federal para consolidar informações sobre segurança pública no Brasil. O SinespJC, criado em 2004, coleta dados de boletins de ocorrência das Polícias Civis, enquanto o Sinesp Integração, lançado em 2015, unifica informações de diferentes fontes para análises mais detalhadas. Os dados incluem registros de crimes como homicídio, furto e roubo de veículos, entre outros. Vale destacar que as informações são atualizadas periodicamente e podem sofrer revisões conforme a validação dos órgãos responsáveis.")


# Definição de perguntas de análise
st.sidebar.header("Perguntas para Análise de Dados")

st.markdown("""
## Perguntas para Análise de Dados

### **Análise Temporal**
1. Como a quantidade de ocorrências de cada tipo de crime variou ao longo dos anos?  
2. Existe uma tendência de aumento ou diminuição de crimes específicos ao longo do tempo?  
3. Quais meses do ano apresentam maior incidência de crimes?  

### **Análise Geográfica**
4. Quais estados apresentam o maior e o menor número de ocorrências criminais?  
5. Como a distribuição de crimes varia entre as regiões do Brasil?  

### **Análise por Tipo de Crime**
6. Qual é o crime mais frequente registrado nos dados?  
7. Algum tipo de crime apresenta variação sazonal ao longo do ano?  

### **Análise de Vítimas**
8. Há diferença entre o número de vítimas masculinas e femininas em cada tipo de crime?  
9. Qual o tipo de crime que mais afeta vítimas do sexo feminino? E do sexo masculino?  
10. Existe alguma relação entre a quantidade de ocorrências e o número de vítimas?  

### **Intervalos de Confiança**
11. Qual o intervalo de confiança de 95% para a média de homicídios nos últimos 5 anos?
12. Qual o intervalo de confiança para a proporção de roubos de veículos em relação ao total de crimes?  
14. Existe uma diferença significativa na média de crimes entre estados do Norte e do Sul?  

### **Testes de Hipótese**
14. A média de homicídios em São Paulo é significativamente maior do que no Rio de Janeiro?  
15. A média de crimes varia entre diferentes regiões do Brasil?
16. O tipo de crime mais frequente muda conforme o estado?
17. Há uma relação significativa entre o sexo da vítima e o tipo de crime?  
""")


st.subheader("Visualização das primeiras linhas do dataset:")
st.write("Visualização dos dados da tabela de ocorrências:")
st.dataframe(df_ocorrencias.head())  # Exibir os dados na tela

st.write("Visualização dos dados da tabela de vítimas:")
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