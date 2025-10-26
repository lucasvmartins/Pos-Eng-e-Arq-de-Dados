# Dataframes com Spark

# %%
# Importando
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName('Dataframes com Spark').getOrCreate()
spark.version

# %%
# Lendo dataframe
sf_call = spark.read.csv('sf-fire-calls.csv', header=True, inferSchema=True)

sf_call.printSchema()

# %%
# Parecido com o pandas
sf_call.head(5)

# %%
# Total de registros
sf_call.count()

# %%
# Usando distinct no tipo de chamada
sf_call.select('CallType').distinct().show()

# %%
# Contando os tipos de chamados
sf_call.select('CallType').distinct().count()

# %%
# Agrupando por tipo de chamada e contando o total de forma ordenada descendente
sf_call.groupBy('CallType').count().sort(col('count').desc()).show()

# %%
# Agrupando por tipo de chamada e unidade e contando o total de forma ordenada descendente
sf_call.groupBy('CallType', 'UnitType').count().sort(col('count').desc()).show()

# %%
# Coluna Renomeada
df_fire = sf_call.withColumnRenamed('Delay', 'ResponseDelayedinMins')

df_fire.printSchema()

# %%
# Contando o total de chamadas com 15min de atraso
df_fire.select('CallNumber', 'ResponseDelayedinMins').where(col('ResponseDelayedinMins') > 15).count()

# %%
df_fire.select('CallType', 'ZipCode')\
        .where(col('CallType').isNotNull())\
        .groupBy('CallType', 'ZipCode')\
        .count().orderBy('count', ascending=False)\
        .show()
