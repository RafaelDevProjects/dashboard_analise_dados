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

# Calcular os intervalos de confiança
confidence_intervals = {}
for state in selected_states:
    confidence_intervals[state] = {}
    for crime in selected_crimes:
        data = df_uf_filtered[(df_uf_filtered['UF'] == state) & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
        mean = np.mean(data)
        sem = stats.sem(data)
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
        confidence_intervals[state][crime] = ci

# Interface Streamlit
st.title('🔍 Análise de Dados de Segurança Pública')

st.header('📊 Intervalos de Confiança')
for state, crimes in confidence_intervals.items():
    st.subheader(f"📍 Estado: {state}")
    for crime, ci in crimes.items():
        ci_rounded = (int(round(ci[0], 0)), int(round(ci[1], 0)))
        st.write(f" **Crime:** {crime} | 📈 **Intervalo de Confiança:** {ci_rounded}")








st.header('📉 Distribuição das Ocorrências de Crimes')

# Filtros interativos
selected_states_multiselect = st.multiselect('🌎 Selecione os Estados', selected_states, default=state_sp_rj)
selected_crime = st.selectbox('🔎 Selecione o Tipo de Crime', selected_crimes)

# Filtrar dados
filtered_data_multiselect = df_uf_filtered[
    (df_uf_filtered['UF'].isin(selected_states_multiselect)) &
    (df_uf_filtered['Tipo Crime'] == selected_crime)
]

# Cores para consistência
palette = sns.color_palette('tab10', len(selected_states_multiselect))
state_colors = dict(zip(selected_states_multiselect, palette))

# Plotar histograma
plt.figure(figsize=(10, 6))
sns.histplot(data=filtered_data_multiselect, x='Ocorrências', kde=True, hue='UF', palette=state_colors)

# Adicionar linhas verticais sem interferir na legenda
for state in selected_states_multiselect:
    data = df_uf_filtered[
        (df_uf_filtered['UF'] == state) & 
        (df_uf_filtered['Tipo Crime'] == selected_crime)
    ]['Ocorrências']

    mean = np.mean(data)
    ci_lower, ci_upper = confidence_intervals[state][selected_crime]
    color = state_colors[state]

    # Linha de média (tracejada)
    plt.axvline(mean, color=color, linestyle='--', linewidth=2)

    # Linhas do intervalo de confiança (pontilhadas)
    plt.axvline(ci_lower, color=color, linestyle=':', linewidth=1.5)
    plt.axvline(ci_upper, color=color, linestyle=':', linewidth=1.5)

# Legenda automática do histograma
plt.title(f'📊 Distribuição das Ocorrências de {selected_crime}')
plt.xlabel('Ocorrências')
plt.ylabel('Frequência')
plt.tight_layout()
st.pyplot(plt)

st.header('🧠 Análise dos Dados')
st.write("""
### Intervalos de Confiança
Os intervalos de confiança fornecem uma estimativa do intervalo onde a **média das ocorrências de crimes** provavelmente está, com **95% de certeza**.

### Distribuição das Ocorrências
Os gráficos mostram como os crimes estão distribuídos nos estados selecionados, ajudando a detectar **padrões**, **picos** ou **anomalias** nas ocorrências.
""")

# Análise detalhada SP x RJ
st.header('⚖️ Análise Detalhada: SP x RJ')
st.write("""
Esta análise compara os estados de **São Paulo** e **Rio de Janeiro** nos tipos de crimes selecionados. 
Os intervalos de confiança ajudam a interpretar se as diferenças são estatisticamente significativas.
""")

for crime in selected_crimes:
    sp_data = df_uf_filtered[(df_uf_filtered['UF'] == 'São Paulo') & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
    rj_data = df_uf_filtered[(df_uf_filtered['UF'] == 'Rio de Janeiro') & (df_uf_filtered['Tipo Crime'] == crime)]['Ocorrências']
    
    sp_mean = np.mean(sp_data)
    rj_mean = np.mean(rj_data)
    
    sp_ci = confidence_intervals['São Paulo'][crime]
    rj_ci = confidence_intervals['Rio de Janeiro'][crime]
    
    st.subheader(f"Crime: {crime}")
    st.write(f"🔵 **São Paulo** - Média: {sp_mean:.2f}, IC: {sp_ci}")
    st.write(f"🔴 **Rio de Janeiro** - Média: {rj_mean:.2f}, IC: {rj_ci}")
    
    if sp_ci[1] < rj_ci[0]:
        st.success("📈 Conclusão: O número médio de ocorrências é significativamente **maior no Rio de Janeiro**.")
    elif rj_ci[1] < sp_ci[0]:
        st.success("📉 Conclusão: O número médio de ocorrências é significativamente **maior em São Paulo**.")
    else:
        st.info("⚖️ Conclusão: **Não há diferença significativa** entre os dois estados nesse crime.")

# Conclusão geral
st.header("📌 Conclusão Geral")
st.write("""
📊 A análise dos dados de segurança pública de **São Paulo** e **Rio de Janeiro** revela que, embora ambos enfrentem desafios, 
existem **diferenças importantes** nas taxas de ocorrência de certos crimes.

📈 Os **intervalos de confiança** ajudam a estimar a média das ocorrências com mais precisão, enquanto os gráficos facilitam a **compreensão visual**.

🛡️ Essas informações são valiosas para orientar **políticas públicas**, priorização de **recursos** e estratégias de **prevenção da criminalidade**.
""")