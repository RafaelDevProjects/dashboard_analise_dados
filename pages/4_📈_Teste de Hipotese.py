import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats


df_uf = pd.read_excel('indicadoressegurancapublicauf.xlsx', engine='openpyxl')

selected_crimes = df_uf['Tipo Crime'].unique()
selected_states = df_uf['UF'].unique()

st.title('Teste de Hipótese - Comparação entre Estados')

crime = st.selectbox('Selecione o crime para análise', selected_crimes)
state1 = st.selectbox('Selecione o primeiro estado', selected_states, index=0)
state2 = st.selectbox('Selecione o segundo estado', selected_states, index=1)

data1 = df_uf[(df_uf['UF'] == state1) & (df_uf['Tipo Crime'] == crime)]['Ocorrências']
data2 = df_uf[(df_uf['UF'] == state2) & (df_uf['Tipo Crime'] == crime)]['Ocorrências']

if len(data1) < 2 or len(data2) < 2:
    st.warning("Não há dados suficientes para realizar o teste de hipótese.")
else:
    st.subheader('Estatísticas Descritivas')
    col1, col2 = st.columns(2)
    col1.metric(f'{state1} - Média', f'{np.mean(data1):.2f}')
    col1.metric(f'{state1} - Desvio Padrão', f'{np.std(data1, ddof=1):.2f}')
    col2.metric(f'{state2} - Média', f'{np.mean(data2):.2f}')
    col2.metric(f'{state2} - Desvio Padrão', f'{np.std(data2, ddof=1):.2f}')

    # Teste t de Student (independente, variâncias iguais ou não)
    st.subheader('Resultado do Teste de Hipótese')
    t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)

    st.write(f"**Hipótese nula (H₀):** As médias de ocorrências são iguais entre {state1} e {state2}")
    st.write(f"**Estatística t:** {t_stat:.4f}")
    st.write(f"**Valor-p:** {p_value:.4f}")

    alpha = 0.05
    if p_value < alpha:
        st.success(f"Rejeitamos H₀: Diferença significativa nas médias de ocorrências para {crime}.")
    else:
        st.info(f"Não rejeitamos H₀: Sem evidência de diferença significativa para {crime}.")
