import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm, poisson, binom


# Carregar os arquivos CSV
df_orders = pd.read_csv("olist_orders_dataset_organizado.csv")
df_order_items = pd.read_csv("olist_order_items_dataset_organizado.csv")
df_customers = pd.read_csv("olist_customers_dataset_organizado.csv")
df_products = pd.read_csv("olist_products_dataset_organizado.csv")
df_sellers = pd.read_csv("olist_sellers_dataset_organizado.csv")

# Juntando as tabelas
df = df_order_items.merge(df_orders, on="order_id", how="inner")
df = df.merge(df_customers, on="customer_id", how="inner")
df = df.merge(df_products, on="product_id", how="inner")
df = df.merge(df_sellers, on="seller_id", how="inner")

# Streamlit - Interface do Dashboard
st.title("Análise do Mercado de E-commerce")

st.sidebar.title("Sumário")
st.sidebar.markdown("[1. Introdução ao Dataset](#introducao-ao-dataset)")
st.sidebar.markdown("[2. Perguntas para Análise](#perguntas-de-analise)")
st.sidebar.markdown("[3. Tipos de Variáveis](#tipos-de-variaveis)")
st.sidebar.markdown("[4. Análise Estatística](#analise-estatistica)")
st.sidebar.markdown("[5. Discusão sobre a distribuição dos dados](#distribuicao-dados)")
st.sidebar.markdown("[6. Distribuições Probabilisticas](#distribuicao-probabilisticas)")



# Apresentação do Dataset
st.header("1. Introdução ao Dataset", anchor="introducao-ao-dataset")
st.write("Este dataset contém informações sobre vendas realizadas no e-commerce Olist, abrangendo pedidos, produtos, clientes e vendedores. Nosso objetivo é explorar padrões de vendas, analisar correlações e entender o comportamento do mercado.")


# Definição de perguntas de análise
st.header("Principais perguntas para análise e respostas:", anchor="perguntas-de-analise")
st.markdown("1. **Qual é a distribuição dos pedidos ao longo do tempo?**\n"
            "   - Os pedidos se concentram em determinados períodos do ano?\n"
            "2. **Qual é o ticket médio das compras?**\n"
            "3. **Quais são as categorias de produtos mais vendidas?**\n"
            "   - Algumas categorias têm maior volume de vendas do que outras?\n"
            "4. **Existe correlação entre o valor do frete e o preço do produto?**\n"
            "5. **Qual é o tempo médio de entrega dos pedidos?**\n"
            "6. **Quais estados/cidades concentram o maior número de compras?**\n")


st.subheader("Visualização das primeiras linhas do dataset:")

df_filtrado = df[['categoria_produto','preco','data_limite_de_envio','valor_frete','status_pedido', 'data_de_compra' ,'data_compra_aprovada' , 'data_entrega_tranpor' ,'data_entregue_cliente','data_estimada_entrega','customer_city','customer_state','comprimento_produto','comprimento_descricao_produto','quantidade_fotos_produto','peso_produto','comprimento_produto_cm','altura_produto_cm','product_largura_cm','cep_vendedor','cidade_vendedor','UF_vendedor']]

st.dataframe(df_filtrado.head())








# Identificação dos tipos de variáveis
st.subheader("Tipos de variáveis no dataset:", anchor="tipos-de-variaveis")
tipo_dados = {
    "order_id": "Qualitativa Nominal",
    "customer_id": "Qualitativa Nominal",
    "status_pedido": "Qualitativa Nominal",
    "data_de_compra": "Quantitativa Contínua",
    "preco": "Quantitativa Contínua",
    "valor_frete": "Quantitativa Contínua",
    "categoria_produto": "Qualitativa Nominal",
    "peso_produto": "Quantitativa Contínua",
    "comprimento_produto_cm": "Quantitativa Contínua",
    "altura_produto_cm": "Quantitativa Contínua",
    "product_largura_cm": "Quantitativa Contínua",
    "customer_city": "Qualitativa Nominal",
    "customer_state": "Qualitativa Nominal",
    "cidade_vendedor": "Qualitativa Nominal",
    "UF_vendedor": "Qualitativa Nominal"
}
st.write(pd.DataFrame(tipo_dados.items(), columns=["Coluna", "Tipo de Dado"]))



# Cálculos Estatísticos (Média, Mediana, Moda, Desvio Padrão, Variância)
st.header("2. Análise Estatística" , anchor="analise-estatistica")
st.markdown("Aqui, vamos calcular a média, mediana, moda, desvio padrão e variância para algumas variáveis numéricas.")

# Cálculos para o preço
preco_media = df["preco"].mean()
preco_mediana = df["preco"].median()
preco_moda = df["preco"].mode()[0]  # Moda pode ter mais de um valor, vamos pegar o primeiro
preco_desvio_padrao = df["preco"].std()
preco_variancia = df["preco"].var()
preco_minimo = df["preco"].min()  # Mínimo preço
preco_maximo = df["preco"].max()  # Máximo preço

# Criando um DataFrame para exibir os resultados
dados_estatisticos = {
    "Métrica": ["Média", "Mediana", "Moda", "Desvio Padrão", "Variância", "Mínimo", "Máximo"],
    "Preço": [preco_media, preco_mediana, preco_moda, preco_desvio_padrao, preco_variancia, preco_minimo, preco_maximo]
}

df_estatisticas = pd.DataFrame(dados_estatisticos)

# Exibindo a tabela com as estatísticas
st.table(df_estatisticas)



st.markdown("1. **Média (120.65):** A média é o valor esperado dos preços dos produtos, considerando todos os itens. Ela é relativamente alta, indicando que, em média, os preços dos produtos são altos. No entanto, é importante observar que a média pode ser influenciada por valores muito altos (outliers).")

st.markdown("2. **Mediana (74.99):** A mediana divide os preços ao meio, ou seja, 50% dos produtos têm preços abaixo de 74.99 e 50% estão acima desse valor. A mediana sendo significativamente mais baixa que a média sugere que a distribuição dos preços é assimétrica, ou seja, tem uma cauda longa para valores mais altos. Isso pode indicar que há poucos produtos com preços muito altos que puxam a média para cima.")

st.markdown("3. **Moda (59.90):** A moda representa o preço que mais se repete. Nesse caso, o preço mais comum dos produtos é 59.90, que é inferior tanto à média quanto à mediana. Isso reforça a ideia de que a maioria dos produtos são vendidos a preços mais baixos, mas que existem alguns itens muito caros que fazem a média ser mais alta.")

st.markdown("4. **Desvio Padrão (183.63):** O desvio padrão indica o quão dispersos os preços estão em relação à média. Com um valor tão alto, isso significa que há uma grande variação nos preços dos produtos. Alguns produtos são vendidos por preços muito mais altos ou muito mais baixos que a média, o que confirma a existência de outliers ou produtos de grande variação de preço.")

st.markdown("5. **Variância (33,721.42):** A variância é a medida quadrada da dispersão. Assim como o desvio padrão, ela indica o quanto os preços variam. Como o desvio padrão é alto e a variância é igualmente grande, isso reforça a ideia de que há uma ampla gama de preços no mercado, com produtos mais caros ou mais baratos.")

st.markdown("6. **Mínimo (0.8500):** O preço mais baixo é R$ 0,85, o que pode indicar a presença de produtos com preços muito baixos, possivelmente promocionais ou de baixo custo. Isso também pode influenciar a média para valores mais baixos, já que a média é sensível a valores extremos.")

st.markdown("7. **Máximo (6,735.0000):** O preço mais alto é R$ 6.735,00, o que é um valor extremamente alto em comparação com a mediana e moda. Esse preço elevado pode estar puxando a média para cima, criando uma distorção nos valores.")

st.markdown("### Conclusão:")

st.write("A análise dos dados sugere que há uma grande disparidade nos preços dos produtos. A média de R$ 120,65 está sendo influenciada por preços muito altos (R$ 6.735,00), enquanto a mediana e a moda indicam que a maior parte dos produtos tem preços muito mais baixos (em torno de R$ 59,90). O grande desvio padrão e variância reforçam que há uma grande variação nos preços, com alguns produtos com preços muito baixos e outros extremamente altos. Isso pode indicar uma estratégia de preços que abrange uma gama muito ampla de produtos, desde os mais baratos até os mais caros.")




# Discussão sobre a distribuição dos dados
st.header(" Discussão sobre a Distribuição dos Dados" , anchor="distribuicao-dados")
st.write("Analisando a distribuição dos preços, podemos observar que é importante verificar se a variável segue uma distribuição normal ou outras distribuições. "
         "A distribuição do preço pode ser assimétrica ou ter outliers que impactam a análise.")

# Plotando histograma para verificar a distribuição dos preços
fig, ax = plt.subplots(figsize=(5, 3))  # Ajustando o tamanho da figura
sns.histplot(df["preco"], kde=True, ax=ax, bins=500)  # Ajustando o número de bins
ax.set_title("Distribuição do Preço dos Produtos")

# Limitando o eixo X para um intervalo de preços mais focado
ax.set_xlim(0, 1000)  # Ajuste o limite de 0 a 500 (exemplo, dependendo da distribuição dos dados)

# Exibindo o gráfico
st.pyplot(fig)

st.markdown("- A distribuição de preços está fortemente inclinada para a direita, com uma concentração de produtos de preços mais baixos, mas também com alguns produtos de preços muito altos, o que aumenta a média e a variância.")

st.markdown("- A moda (preço mais frequente) sendo mais baixa que a média também reforça a ideia de que a maioria dos preços é relativamente baixa, mas que a base de dados contém uma minoria de itens muito caros.")

st.markdown("- O alto desvio padrão e a variância indicam que o portfólio de produtos tem uma grande diversidade de preços.")




st.header("Os pedidos se concentram em determinados períodos do ano?")
# Gráfico de Pedidos ao Longo do Tempo
df["data_de_compra"] = pd.to_datetime(df["data_de_compra"])
df["year_month"] = df["data_de_compra"].dt.to_period("M")
pedidos_por_mes = df.groupby("year_month").size()
fig, ax = plt.subplots()
pedidos_por_mes.plot(kind="line", ax=ax)


ax.set_title("Evolução dos Pedidos ao Longo do Tempo")
ax.set_xlabel("Ano-Mês")
ax.set_ylabel("Quantidade de Pedidos")
st.pyplot(fig)

st.markdown("### Análise do Gráfico de Evolução dos Pedidos:")
st.markdown("1. **Outubro de 2016 até Janeiro de 2018:** O gráfico começa com vendas baixas, indicando uma fase inicial de crescimento ou introdução ao mercado. A partir de então, há um crescimento gradual nas vendas, sugerindo que a empresa começou a ganhar tração.")

st.markdown("2. **Pico de Vendas em Janeiro de 2018:** O pico indica um aumento significativo nas vendas, possivelmente por campanhas de marketing ou promoções de início de ano. Esse pico é um marco importante de sucesso.")

st.markdown("3. **Estabilidade de Fevereiro a Julho de 2018:** Após o pico, as vendas se estabilizam, indicando uma fase de maturação no mercado. A empresa mantém uma base de clientes, mas sem grandes variações no número de pedidos.")

st.markdown("#### Implicações:")
st.markdown("- O pico em 2018 pode ser replicado com estratégias semelhantes.")
st.markdown("- A estabilidade sugere que é hora de inovar ou diversificar para evitar estagnação.")







# Gráfico de Categorias mais Vendidas
st.header("Quais são as categorias de produtos mais vendidas?")
categorias_mais_vendidas = df["categoria_produto"].value_counts().head(10)
fig, ax = plt.subplots()
categorias_mais_vendidas.plot(kind="bar", ax=ax)
ax.set_title("Top 10 Categorias Mais Vendidas")
ax.set_xlabel("Categoria")
ax.set_ylabel("Quantidade de Vendas")
st.pyplot(fig)

st.markdown("#### Implicações:")
st.markdown("- As categorias mais vendidas mostram um claro foco em bem-estar, conforto e lazer, com destaque para itens essenciais de casa e cuidados pessoais.")
st.markdown("- Produtos de tecnologia e eletrônicos também desempenham um papel significativo, refletindo a busca contínua por inovações e conectividade.")
st.markdown("- Móveis e decoração indicam que os consumidores estão cada vez mais preocupados em tornar seus lares confortáveis e esteticamente agradáveis.")
st.markdown("- A categoria automotiva, embora com menos vendas, ainda representa um mercado com um público fiel e especializado")





st.header("Qual é o ticket médio das compras?")
st.markdown("   - Ticket médio é calculado como o valor total dos pedidos dividido pelo número de pedidos.\n"
            "   - O valor médio gasto por pedido está mostrado abaixo.")


ticket_medio = df["preco"].mean()
st.write(f"O ticket médio das compras é **R${ticket_medio:.2f}**.")

st.markdown("O ticket médio de R$120,65 significa que, em média, cada cliente gasta esse valor por pedido. Esse valor pode indicar que os consumidores estão comprando produtos de médio porte ou uma combinação de itens de baixo e alto valor. Se comparado com os preços das categorias mais vendidas, esse ticket médio pode refletir a compra de produtos essenciais como itens de cama, mesa e banho e beleza e saúde, que geralmente têm um preço mais acessível, junto com compras ocasionais de produtos de maior valor, como eletrônicos ou móveis.")




st.header("Existe correlação entre o valor do frete e o preço do produto?")
st.markdown( "   - A correlação entre essas variáveis pode indicar padrões de precificação.")

# Correlação entre preço e frete
correlacao_frete_preco = df[["preco", "valor_frete"]].corr().iloc[0,1]
st.write(f"A correlação entre o valor do frete e o preço do produto é **{correlacao_frete_preco:.2f}**.")
st.markdown("A correlação de 0.41 entre o valor do frete e o preço do produto sugere uma correlação moderada e positiva, ou seja, quando o preço do produto aumenta, o valor do frete tende a ser maior também. Isso pode ocorrer devido ao peso, volume ou distância de entrega de produtos mais caros, que geralmente são mais pesados ou têm maior volume. No entanto, como a correlação não é muito forte, outros fatores, como políticas de frete ou descontos, podem também influenciar o valor final do frete.")




st.header("Qual é o tempo médio de entrega dos pedidos?")
st.markdown("   - O tempo médio entre a compra e a entrega final.")
df["data_estimada_entrega"] = pd.to_datetime(df["data_estimada_entrega"])
df["tempo_entrega"] = (df["data_estimada_entrega"] - df["data_de_compra"]).dt.days
tempo_medio_entrega = df["tempo_entrega"].mean()
st.write(f"O tempo médio de entrega dos pedidos é **{tempo_medio_entrega:.2f} dias**.")

st.markdown("O tempo médio de entrega de 23,47 dias indica que, em média, os clientes recebem seus pedidos cerca de 23 dias após a compra. Esse tempo pode ser considerado relativamente longo dependendo do setor e da expectativa dos consumidores. Melhorias no processo logístico, como otimização de rotas ou parcerias com transportadoras mais rápidas, podem ser uma oportunidade para reduzir esse tempo e melhorar a experiência do cliente.")







st.header("Quais estados/cidades concentram o maior número de compras?")
st.markdown("   - Abaixo, os estados com maior volume de pedidos.")

# Estados com mais pedidos
estados_mais_pedidos = df["customer_state"].value_counts().head(10)
fig, ax = plt.subplots()
estados_mais_pedidos.plot(kind="bar", ax=ax)
ax.set_title("Top 10 Estados com Mais Pedidos")
ax.set_xlabel("Estado")
ax.set_ylabel("Quantidade de Pedidos")
st.pyplot(fig)

st.markdown("Os top 10 estados com mais pedidos mostram que São Paulo, Rio de Janeiro e Minas Gerais são os principais responsáveis pelas compras, refletindo a maior concentração de consumidores. Rio Grande do Sul e Espírito Santo também se destacam, indicando uma boa distribuição das vendas pelo Brasil. Isso sugere que as estratégias de marketing e logística podem ser otimizadas para focar nessas regiões com maior volume de pedidos.")





st.write("A próxima etapa será aplicar distribuições probabilísticas para aprofundar nossa análise!")


# Aplicação de Distribuições Probabilísticas
st.header("3. Aplicação de Distribuições Probabilísticas", anchor="distribuicao-probabilisticas")
st.write("Aqui aplicamos duas distribuições probabilísticas (Normal e Poisson) para modelar características do nosso dataset.")

# 1. Distribuição Normal aplicada ao preço dos produtos
st.subheader("Distribuição Normal do Preço dos Produtos")
st.write("A distribuição normal é usada para modelar fenômenos que seguem um comportamento simétrico em torno de uma média. Como os preços dos produtos variam amplamente e tendem a ter uma concentração em torno de um valor médio, essa distribuição é adequada.")

# Parâmetros da distribuição normal
mu, sigma = df["preco"].mean(), df["preco"].std()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = norm.pdf(x, mu, sigma)

# Plotando a distribuição normal
fig, ax = plt.subplots()
ax.plot(x, y, label=f"Normal (µ={mu:.2f}, σ={sigma:.2f})")
sns.histplot(df["preco"], kde=True, stat="density", bins=30, ax=ax)
ax.set_title("Distribuição Normal do Preço dos Produtos")
ax.set_xlabel("Preço")
ax.set_ylabel("Densidade")
ax.legend()
st.pyplot(fig)

st.markdown("### Interpretação:")
st.markdown("- A curva normal ajustada indica que a maioria dos preços está concentrada em torno da média, com uma dispersão característica da distribuição normal.")
st.markdown("- Entretanto, a presença de valores muito altos ou baixos pode causar assimetrias na distribuição real dos dados.")

# 2. Distribuição de Poisson aplicada ao número de pedidos por dia
st.subheader("Distribuição de Poisson para Número de Pedidos por Dia")
st.write("A distribuição de Poisson é usada para modelar eventos raros que ocorrem dentro de um intervalo fixo de tempo. Como estamos analisando o número de pedidos realizados por dia, essa distribuição se encaixa bem para entender a frequência dos pedidos.")

# Contagem de pedidos por dia
df["data_de_compra"] = pd.to_datetime(df["data_de_compra"])
pedidos_por_dia = df["data_de_compra"].dt.date.value_counts().sort_index()
media_pedidos_dia = pedidos_por_dia.mean()
x_poisson = np.arange(0, max(pedidos_por_dia)+1)
y_poisson = poisson.pmf(x_poisson, media_pedidos_dia)

# Plotando a distribuição de Poisson
fig, ax = plt.subplots()
ax.bar(x_poisson, y_poisson, label=f"Poisson (λ={media_pedidos_dia:.2f})", alpha=0.6)
sns.histplot(pedidos_por_dia, kde=False, stat="density", bins=30, ax=ax)
ax.set_title("Distribuição de Poisson do Número de Pedidos por Dia")
ax.set_xlabel("Número de Pedidos por Dia")
ax.set_ylabel("Probabilidade")
ax.legend()
st.pyplot(fig)

st.markdown("### Interpretação:")
st.markdown("- A distribuição de Poisson ajustada reflete a frequência de pedidos diários, mostrando a probabilidade de ocorrerem diferentes quantidades de pedidos em um dia.")
st.markdown("- O pico da distribuição indica o número de pedidos mais comum por dia, enquanto valores muito altos ou baixos são menos prováveis.")

st.write("Com essas distribuições probabilísticas, conseguimos entender melhor os padrões de preços dos produtos e a frequência de pedidos no e-commerce.")
