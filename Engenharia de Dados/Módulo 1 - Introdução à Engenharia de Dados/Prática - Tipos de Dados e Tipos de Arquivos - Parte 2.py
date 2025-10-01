# %%
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# %%
spark = SparkSession.builder.appName("aula.filetypes").getOrCreate()
file_name = 'Online-sales'

df = spark.read.csv(f'{file_name}.csv', header=True, sep=';', encoding='ISO-8859-1')

df.head()

# %%
df.printSchema()

# %%
df.printSchema()

# %%
df.columns

# %%
df_tratado = df.select([F.col(x).alias(x.replace('-', '').replace(' ', '_').lower()) for x in df.columns])

print(df_tratado)
df_tratado.columns

# %%
#  -  - 
df_tratado = df_tratado.withColumn('price', F.expr("cast(replace(price, ',', '.') as float)"))\
                        .withColumn('value', F.expr("cast(replace(value, ',', '.') as float)"))\
                        .withColumn('total', F.expr("cast(replace(total, ',', '.') as float)"))

# %%
df_tratado.printSchema()

# %%
df_tratado.show()

# %%
df_tratado.write.mode("overwrite").parquet(f"{file_name}.parquet")

# %%
df_pqt = spark.read.parquet(f'{file_name}.parquet')
df_pqt.printSchema()