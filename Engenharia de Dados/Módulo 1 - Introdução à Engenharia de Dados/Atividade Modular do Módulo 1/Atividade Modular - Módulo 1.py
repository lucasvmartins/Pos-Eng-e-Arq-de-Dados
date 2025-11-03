# Atividade Módular - Módulo 1

# %%
import pandas as pd

# %%
# Lendo o arquivo CSV
dados = 'Iris'

df = pd.read_csv(f'{dados}.csv', sep=',', index_col='Id')

# %%
# Exibindo as 5 primeiras linhas
df.head()

# %%
# Mostrando o formato dos dados
df.shape

# %%
# Exibindo as colunas e seus formatos de dados
df.info()

# %%
# Resumo estatístico dos dados
df.describe()

# %%
# Verificando se há alguma coluna com dados faltantes
df.isnull().sum()

# %%
# Explorando a quantidade de espécies individuais no dataset
data = df.drop_duplicates(subset='Species')
data

# %%
# Verificando a quantidade de cada espécie para saber o balanceamento do dataset
df.value_counts('Species')

# %%
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# Plotando os dados do dataset
sns.countplot(x='Species', data=df,)
plt.show()  # Quantidade de cada espécie

# %%
sns.scatterplot(x='SepalLengthCm', y='SepalWidthCm', hue='Species', data=df)    # Diferenças entre relação entre o comprimento e a largura da sépala

# Colocando a legenda fora da figura
# plt.legend(bbox_to_anchor=(1, 1), loc=2)
# plt.show()

# %%
# Diferenças entre relação entre o comprimento e a largura da pétala
sns.scatterplot(x='PetalLengthCm', y='PetalWidthCm', hue='Species', data=df)

# %%
# Representando graficamente todos os relacionamentos do dataset utilizando pairplot
sns.pairplot(df, hue='Species', height=2)

# %%
# Distribuição dos dados nas colunas utilizando histogramas

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0,0].set_title('Sepal Lenght')
axes[0,0].hist(df['SepalLengthCm'], bins=7)

axes[0, 1].set_title('Sepal Width')
axes[0, 1].hist(df['SepalWidthCm'], bins=5)

axes[1, 0].set_title('Petal Length')
axes[1, 0].hist(df['PetalLengthCm'], bins=6)

axes[1, 1].set_title('Petal Width')
axes[1, 1].hist(df['PetalWidthCm'], bins=6)

# %%
# Histogramas utilizando Distplot

plot = sns.FacetGrid(df, hue='Species')
plot.map(sns.displot, 'SepalLengthCm').add_legend()

plot = sns.FacetGrid(df, hue='Species')
plot.map(sns.displot, 'SepalWidthCm').add_legend()

plot = sns.FacetGrid(df, hue='Species')
plot.map(sns.displot, 'PetalLengthCm').add_legend()

plot = sns.FacetGrid(df, hue='Species')
plot.map(sns.displot, 'PetalWidthCm').add_legend()

plot.show()

# %%
# Análises de correlações dos pares de coluna do dataset
data.corr(method='pearson')

sns.heatmap(df.corr(method='pearson'))
plt.show()

# %%
# Identificando outliers no conjunto de dados

def graph(y):
    sns.boxplot(x='Species', y=y, data=df)

plt.figure(figsize=(10, 10))

# Adicionando subplot na posição específica
plt.subplot(221)
graph('SepalLengthCm')

plt.subplot(222)
graph('SepalWidthCm')

plt.subplot(223)
graph('PetalLengthCm')

plt.subplot(224)
graph('PetalWidthCm')

plt.show()
