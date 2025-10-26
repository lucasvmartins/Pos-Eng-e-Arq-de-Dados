# Prática de SQL com Spark

# %%
# Importando biblioteca, criando sessão e lendo Dataframe
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName('SQL com Spark').getOrCreate()
spark.active()

# %%
sf_calls = spark.read.csv('..\Prática - Dataframes com Spark\sf-fire-calls.csv', header=True, inferSchema=True)

sf_calls.printSchema()

# %%
sf_calls.head(5)

# %%
sf_calls.count()

# %%
# Criando uma tabela e usando SQL
sf_calls.createOrReplaceTempView('fire_table')

spark.sql('SELECT COUNT(*) FROM fire_table').show()

# %%
# Usando dataframe do Spark
sf_calls.select('CallType').distinct().show()

# %%
# Usando consulta SQL
spark.sql('SELECT distinct(CallType) FROM fire_table').show()

# %%
# Agrupando por CallType e contando de forma ordenada descrescente
sf_calls.groupBy('CallType').count().sort(col('count').desc()).show()

# %%
# O mesmo comando mas usando SQL
spark.sql('SELECT CallType, COUNT(*) AS COUNT from fire_table \
          GROUP BY CallType ORDER BY COUNT DESC').show()

# %%
# Renomeando coluna e remontando a tabela
sf_calls = sf_calls.withColumnRenamed('Delay', 'ResponseDelayinMins')
sf_calls.createOrReplaceTempView('fire_table')

spark.sql('SELECT CallType, ResponseDelayinMins FROM fire_table \
          WHERE ResponseDelayinMins > 50')
