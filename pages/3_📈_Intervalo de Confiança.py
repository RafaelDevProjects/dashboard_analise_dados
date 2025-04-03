import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados dos arquivos Excel
df_uf = pd.read_excel('indicadoressegurancapublicauf.xlsx', engine='openpyxl')
df_munic = pd.read_excel('indicadoressegurancapublicamunic.xlsx', engine='openpyxl')

# Filtrar os dados para os estados e crimes selecionados
selected_states = ['Rio de Janeiro', 'Distrito Federal', 'São Paulo', 'Santa Catarina', 'Bahia']
state_sp_rj = ['São Paulo', 'Rio de Janeiro']
selected_crimes = ['Homicídio doloso', 'Tentativa de homicídio', 'Estupro', 'Furto de veículo']

df_uf_filtered = df_uf[(df_uf['UF'].isin(selected_states)) & (df_uf['Tipo Crime'].isin(selected_crimes))]

# Calcular os intervalos de confiança para cada estado e crime
confidence_intervals = {}

for state in selected_states:
    confidence_intervals[state] = {}
    for crime in selected_crimes:
        data = df_uf_filtered[(df_uf_filtered['UF'] == state) & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
        mean = np.mean(data)
        sem = stats.sem(data)
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
        confidence_intervals[state][crime] = ci

# Aplicativo Streamlit
st.title('Análise de Dados de Segurança Pública')

st.header('Intervalos de Confiança')
for state, crimes in confidence_intervals.items():
    st.subheader(f"Estado: {state}")
    for crime, ci in crimes.items():
        st.write(f"  Crime: {crime}, Intervalo de Confiança: {ci}")

st.header('Distribuição das Ocorrências de Crimes')

# Multiselect para selecionar os estados e selectbox para selecionar o crime
selected_states_multiselect = st.multiselect('Selecione os Estados', selected_states, default=state_sp_rj)
selected_crime = st.selectbox('Selecione o Crime', selected_crimes)

# Filtrar os dados com base na seleção
filtered_data_multiselect = df_uf_filtered[(df_uf_filtered['UF'].isin(selected_states_multiselect)) & (df_uf_filtered['Tipo Crime'] == selected_crime)]

# Plotar o gráfico de distribuição
plt.figure(figsize=(10, 6))
sns.histplot(data=filtered_data_multiselect, x='Ocorrências', kde=True, hue='UF')
plt.title(f'Distribuição das Ocorrências de {selected_crime} em São Paulo e Rio de Janeiro')
plt.xlabel('Ocorrências')
plt.ylabel('Frequência')
st.pyplot(plt)

st.header('Análise dos Dados')
st.write("""
Esta análise foi realizada com base nos dados de segurança pública dos estados de São Paulo e Rio de Janeiro para os tipos de crimes escolhidos. 
Os intervalos de confiança foram calculados para cada estado e tipo de crime, permitindo uma comparação entre eles.

### Intervalos de Confiança
Os intervalos de confiança fornecem uma estimativa do intervalo dentro do qual a média das ocorrências de crimes está localizada com 95% de confiança. 
Isso significa que há uma probabilidade de 95% de que a média real das ocorrências esteja dentro desse intervalo.

### Distribuição das Ocorrências
Os gráficos mostram a distribuição das ocorrências dos crimes para os estados e tipos de crimes selecionados. 
A análise visual desses gráficos pode ajudar a identificar padrões e tendências nos dados, como a frequência e a variação das ocorrências.

### Comparação entre São Paulo e Rio de Janeiro
A comparação entre os estados pode revelar diferenças significativas nas taxas de criminalidade. 
Por exemplo, pode-se observar que o estado do Rio de Janeiro tem um número significativamente maior de furtos de veículos em comparação com São Paulo.

### Conclusão
A análise dos dados de segurança pública de São Paulo e Rio de Janeiro revela que, embora ambos os estados enfrentem desafios significativos em termos de criminalidade, há diferenças notáveis nas taxas de ocorrência de certos crimes. 
Os intervalos de confiança fornecem uma visão mais precisa das médias das ocorrências, permitindo uma melhor compreensão das tendências e padrões de criminalidade em cada estado. 
Essas informações podem ser úteis para direcionar políticas públicas e recursos de segurança de maneira mais eficaz.
""")

# Análise detalhada dos crimes em São Paulo e Rio de Janeiro

st.header('Análise Detalhada dos Crimes em São Paulo e Rio de Janeiro')

for crime in selected_crimes:
    sp_data = df_uf_filtered[(df_uf_filtered['UF'] == 'São Paulo') & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
    rj_data = df_uf_filtered[(df_uf_filtered['UF'] == 'Rio de Janeiro') & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
    
    sp_mean = np.mean(sp_data)
    rj_mean = np.mean(rj_data)
    
    sp_ci = confidence_intervals['São Paulo'][crime]
    rj_ci = confidence_intervals['Rio de Janeiro'][crime]
    
    st.subheader(f"Crime: {crime}")
    st.write(f"São Paulo - Média: {sp_mean:.2f}, Intervalo de Confiança: {sp_ci}")
    st.write(f"Rio de Janeiro - Média: {rj_mean:.2f}, Intervalo de Confiança: {rj_ci}")
    
    if sp_ci[1] < rj_ci[0]:
        st.write("Conclusão: O número médio de ocorrências desse crime é significativamente maior no Rio de Janeiro do que em São Paulo.")
    elif rj_ci[1] < sp_ci[0]:
        st.write("Conclusão: O número médio de ocorrências desse crime é significativamente maior em São Paulo do que no Rio de Janeiro.")
    else:
        st.write("Conclusão: Não há diferença significativa no número médio de ocorrências desse crime entre São Paulo e Rio de Janeiro.")