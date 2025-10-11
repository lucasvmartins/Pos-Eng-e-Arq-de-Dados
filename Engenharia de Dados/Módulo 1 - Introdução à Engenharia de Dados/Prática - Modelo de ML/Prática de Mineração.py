# Prática de Mineração de Dados
# Análise de Risco - Mal Pagadores

# Dados gerados a partir do ChatGPT

# (Os datasets gerados apresentam alguma questão (acredito que de idade) 
# na qual as análises não saíram iguais as da aula, levando todas as análises
# a serem rotuladas como 'Provável Mal Pagador' ou 'Pagador Regular')

# %%
# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, StandardScaler
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

pd.set_option('display.max_colwidth', 150)
pd.set_option('display.min_rows', 20)

# %%
# Lendo o dataset de treino
df = pd.read_csv('dataset_empregados_treino.csv')
df.head()
df.info()


# %%
# Pre-processando os dados
label_encoders = {}
for column in ['Sexo', 'Profissão', 'Estado Civil']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

df.fillna({'Data de Início no Último Emprego': pd.to_datetime('2000-01-01')}, inplace=True)
df['Data de Início no Último Emprego'] = pd.to_datetime(df['Data de Início no Último Emprego'])
df['Anos Empregado'] = (pd.to_datetime('today') - df['Data de Início no Último Emprego']).dt.days // 365
df

# %%
# Adicionando condições de risco
df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'])
df['Idade'] = (datetime.now() - df['Data de Nascimento']).dt.days // 365

# Definindo fatores de risco (Idade, Emprego, Sexo)
def calculo_de_risco(row):
    risco = 0

    # Risco baseado na idade
    if 18 <= row['Idade'] <= 24:
        risco += 1                  # Risco médio
    elif 25 <= row['Idade'] <= 49:
        risco -= 1                  # Risco baixo
    else:
        risco += 1                  # Risco médio

    # Risco com base no emprego (se a data de início for nula '2000-01-01')
    if row['Data de Início no Último Emprego'] == pd.to_datetime('2000-01-01'):
        risco += 4                  # Risco alto (aumenta o risco em 80%)

    # Se for homem o risco aumenta em 5%
    if row['Sexo'] == 1:    # Após a rotulação de categoria, 'Masculino'passa a ser 1
        risco += 0.05

    return risco

df['Risco'] = df.apply(calculo_de_risco, axis=1)

# Somando o risco ao score de crédito
df['Score Ajustado'] = 500 + (df['Risco'] * 50) # Inicializa um novo score base em 500
df['Score Ajustado'] = df['Score Ajustado'].clip(lower=0, upper=850)
df

# %%
# Transformando o score ajustado em classes
def categorizando_score(score):
    if score > 550:
        return 1                # Bom pagador
    elif 450 < score <= 550:
        return 0                # Pagador regular
    else:
        return -1               # Mal pagador

# Aplicando a categoria
df['Classificação'] = df['Score Ajustado'].apply(categorizando_score)

# Separando em variáveis de entrada e variável alvo
X = df.drop(columns=['Score Ajustado', 'Classificação', 'Nome', 'Data de Nascimento', 'Data de Início no Último Emprego'])
y = df['Classificação']

df

# %%
# Normalização dos Dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividindo o dataset em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# %%
# Treino e teste com KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

# %%
# Treino e teste com Árvore de Decisão
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)

# %%
# Comparando os modelos
print('Resultado do KNN:')
print(classification_report(y_test, y_pred_knn))

print('Resultado da Árvore de Decisão:')
print(classification_report(y_test, y_pred_tree))

# %%
# Boxplot para verificando outliers
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['Salário atual', 'Anos Empregado']])
plt.title('Detecção de Outliers - Salário Atual e Anos no Emprego')
plt.show()

# %%
# Aplicando K-Means para visualizar clusters de clientes
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Clusterização com K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_pca)

plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')
plt.title('Clusterização de Cliente - K-Means')
plt.xlabel('Componente principal 1')
plt.ylabel('Componente principal 2')
plt.show()

# %%
# Utilizando DBScan para análise de quadrantes
dbscan = DBSCAN(eps=0.5, min_samples=5)
db_clusters = dbscan.fit_predict(X_pca)

plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=db_clusters, cmap='plasma')
plt.title('DBScan Para Análise de Quadrantes')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.show()

# %%
# Testando os modelos treinados com o dataset de teste

# Carregando o dataset de teste
df_teste = pd.read_csv('dataset_empregados_teste.csv')

# %%
df_teste.head()
df_teste.info()

# %%
# Preprocessando novos dados
df_teste['Data de Nascimento'] = pd.to_datetime(df_teste['Data de Nascimento'])
df_teste['Data de Início no Último Emprego'] = pd.to_datetime(df_teste['Data de Início no Último Emprego'])
df_teste.fillna({'Data de Início no Último Emprego': pd.to_datetime('2000-01-01')}, inplace=True)
df_teste['Idade'] = (datetime.now() - df_teste['Data de Nascimento']).dt.days // 365
df_teste['Anos Empregado'] = (pd.to_datetime('today') - df_teste['Data de Início no Último Emprego']).dt.days // 365
df_teste['Risco'] = df_teste.apply(calculo_de_risco, axis=1)
df_teste['Score Ajustado'] = df_teste['Score de Crédito'] + (df_teste['Risco'] * 50)
df_teste['Score Ajustado'] = df_teste['Score Ajustado'].clip(lower=0, upper=850)
df_teste['Classificação'] = df_teste['Score Ajustado'].apply(categorizando_score)

# %%
# Separando em variáveis de entrada e variável alvo do novo dataset
X_teste = df_teste[['Sexo', 'Profissão', 'Salário atual', 'Estado Civil', 'Número de Filhos', 'Empregado', 'Idade', 'Anos Empregado']]
X_teste = pd.get_dummies(X_teste, drop_first=True)  # Fazendo o One-hot encoding para variáveis categóricas

# %%
# Ajustando a ordem das colunas para a mesma do dataset de treino
X_teste = X_teste.reindex(columns=X.columns, fill_value=0)  # Preenche com 0 as colunas que não estão no teste
X_teste_scaled = scaler.transform(X_teste)  # Normalizando os dados do dataset de teste

# %%
# Realizando previsões no novo dataset
predicoes_knn = knn.predict(X_teste_scaled)
predicoes_tree = tree.predict(X_teste_scaled)

# %%
# Adicionando as previsões ao dataframe
df_teste['Predição KNN'] = predicoes_knn
df_teste['Predição Árvore'] = predicoes_tree

df_teste

# %%
# Função para mapear as predições feitas
def mapear_predicao(pred):
    if pred == 1:
        return 'Provável Bom Pagador'
    elif pred == 0:
        return 'Provável Pagador Regular'
    else:
        return 'Provável Mal Pagador'

# %%
# Aplicando mapeamento
df_teste['Predição KNN'] = df_teste['Predição KNN'].apply(mapear_predicao)
df_teste['Predição Árvore'] = df_teste['Predição Árvore'].apply(mapear_predicao)

print('Resultados previstos:')
df_teste[['Nome', 'Predição KNN', 'Predição Árvore']]

# %%
# Exportando CSV
df_teste[['Nome', 'Sexo', 'Profissão', 'Salário atual', 'Estado Civil', 'Predição KNN', 'Predição Árvore']].to_csv('Resultados das Análises Preditivas.csv', index=True)
