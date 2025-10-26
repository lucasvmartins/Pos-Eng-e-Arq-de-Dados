# Estatística Descritiva com Spark

# %%
# Importando biblioteca
from pyspark.sql import SparkSession

spark  = SparkSession.builder.appName('Estatística Descritiva com Spark').getOrCreate()
spark.version

# %%
# Lendo arquivo
sf_call = spark.read.csv('..\Prática - Dataframes com Spark\sf-fire-calls.csv', header=True, inferSchema=True)
sf_call.printSchema(5)

# %%
sf_call.head(5)

# %%
# Renomeando coluna
sf_call = sf_call.withColumnRenamed('Delay', 'ResponseDelayedinMins')

# %%
# Descrição do atraso de atendimento
sf_call.describe(['ResponseDelayedinMins']).show()

# %%
# Sumário do atraso de atendimento
sf_call.select('ResponseDelayedinMins').summary().show()

# %%
sf_call.select('NumAlarms').summary().show()
