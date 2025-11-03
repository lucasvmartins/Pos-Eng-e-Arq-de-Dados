# Atividade Modular do Módulo 3
# Analisando dados de cadastro de estabelecimentos brasileiros
# O enunciado para a atividade está em https://drive.google.com/file/d/1GGCAPSSUR9WEuqMvM19TsUCk6s__kHW8/view?usp=sharing
# e as pastas dos dados estão em http://www.dcc.ufmg.br/~pcalais/XPE/engenharia-dados/big-data-spark/desafio

# %%
# Importando bibliotecas e criando sessão Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Atividade Modular do Módulo 3').getOrCreate()
spark.sparkContext

# %%
# Lendo arquivos estabelecimentos 1
df_estab = spark.read.csv('dados\estabelecimentos\estabelecimentos\estabelecimentos-1.csv', sep=';', header=True, inferSchema=True)
df_estab.printSchema()
df_estab.count()

# %%
# Lendo arquivos estabelecimentos 2
df_estab2 = spark.read.csv('dados\estabelecimentos\estabelecimentos\estabelecimentos-2.csv', sep=';', header=True, inferSchema=True)
df_estab2.printSchema()
df_estab2.count()

# %%
# Lendo arquivos estabelecimentos 3
df_estab3 = spark.read.csv('dados\estabelecimentos\estabelecimentos\estabelecimentos-3.csv', sep=';', header=True, inferSchema=True)
df_estab3.printSchema()
df_estab3.count()

# %%
# Unindo dataframe 1, 2 e 3
dataframe = df_estab.union(df_estab2).union(df_estab3)
dataframe.printSchema()
print(f'Quantidade total de estabelecimentos: {dataframe.count()}')

# %%
# Quantidade de colunas e quantidade de colunas do tipo inteiro
print(f'Quantidade de colunas: {len(dataframe.columns)}')
print
num_cols_int = len([c for c, t in dataframe.dtypes if t.startswith("int")])
print(f'Quantidade de colunas do tipo "int": {num_cols_int + 1}')

# %%
# Criando uma tabela temporária
dataframe.createOrReplaceTempView("estabelecimentos")

# %%
# Gerando arquivo parquet
# dataframe.write.mode('overwrite').parquet('estabelecimentos.parquet')

# %%
# Quantos estabelecimentos tem o logradouro nulo
spark.sql('SELECT COUNT(*) FROM estabelecimentos WHERE LOGRADOURO IS NULL').show()

# %%
# Criando a UDF para saber quantos estabelecimentos ficam localizados em uma avenida
def is_avenida(logradouro):
    if logradouro is None:
        return False
    return logradouro.strip().upper().startswith("AVENIDA")

# %%
# Registrando a função
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

spark.udf.register("is_avenida", is_avenida, BooleanType())

# %%
# Atualizando a tabela temporária
dataframe.createOrReplaceTempView("estabelecimentos")

# %%
# Quantos quantos estabelecimentos ficam localizados em uma avenida
spark.sql('''
    SELECT COUNT(*) AS total_avenidas
    FROM estabelecimentos
    WHERE is_avenida(LOGRADOURO) = TRUE
''').show()

# %%
# Quantos CEPs distintos existem entre os estabelecimentos

spark.sql("""
    SELECT COUNT(DISTINCT(CEP)) AS total_de_ceps
    FROM estabelecimentos
""").show()

# %%
# Lendo base de dados do CNAE
df_cnae = spark.read.csv('dados\cnaes\cnaes.csv', sep=';', header=True, inferSchema=True)
df_cnae.printSchema()
df_cnae.count()

# %%
# Join do dataframe com base de dados do CNAE e criação da tabela temporária do join
estabelecimentos_with_cnae = dataframe.join(df_cnae)
df_cnae.createOrReplaceTempView('estabelecimentos_with_cnae')

# %%
# Criação de UDF que verifica se a descrição do CNAE é sobre cultivo
# e registro da função
def is_cnae_cultivo(descricao_cnae):
    if descricao_cnae is None:
        return False
    return 'CULTIVO' in descricao_cnae.strip().upper()


spark.udf.register("is_cnae_cultivo", is_cnae_cultivo, BooleanType())

# %%
# Quantos estabelecimentos possuem um CNAE relacionado a cultivo?
spark.sql("""
    SELECT COUNT(*) AS total_cultivo
    FROM estabelecimentos_with_cnae
    WHERE is_cnae_cultivo(DESCRICAO_CNAE) = TRUE
""").show()

# %%
spark.sql("""
    SELECT COUNT(*) AS total_filiais
    FROM estabelecimentos
    WHERE IDENTIFICADOR_MATRIZ_FILIAL == 2
""").show()

# %%
print('Respostas das questões da atividade modular do módulo 3:')

print(f'Quantidade total de estabelecimentos: {dataframe.count()}\n')

print(f'Quantidade de colunas: {len(dataframe.columns)}')
num_cols_int = len([c for c, t in dataframe.dtypes if t.startswith("int")])
print(f'Quantidade de colunas do tipo "int": {num_cols_int + 1}\n')

print('A economia de espaço entre a diferença dos arquivos no formato \
.csv como estão e o novo formato .parquet foi da \
ordem de 2,5 vezes menos espaço.\n')

print('Quantos estabelecimentos não tem logradouro cadastrado:')
spark.sql('SELECT COUNT(*) FROM estabelecimentos WHERE LOGRADOURO IS NULL').show()

print('Quantos estabelecimentos ficam localizados em uma avenida:')
spark.sql('''
    SELECT COUNT(*) AS total_avenidas
    FROM estabelecimentos
    WHERE is_avenida(LOGRADOURO) = TRUE
''').show()

print('Quantos CEPs distintos existem entre os estabelecimentos')
spark.sql('''
    SELECT COUNT(DISTINCT CEP) as total_de_ceps
    FROM estabelecimentos
''').show()

print(f'Quantos CNAEs existem na tabela de CNAES? \n{df_cnae.count()}\n')

print('Quantos estabelecimentos possuem um CNAE relacionado a cultivo?')
spark.sql("""
    SELECT COUNT(*) AS total_cultivo
    FROM estabelecimentos_with_cnae
    WHERE is_cnae_cultivo(DESCRICAO_CNAE) = TRUE
""").show()

print('Quantos estabelecimentos são filiais?')
spark.sql("""
    SELECT COUNT(*) AS total_filiais
    FROM estabelecimentos
    WHERE IDENTIFICADOR_MATRIZ_FILIAL == 2
""").show()
