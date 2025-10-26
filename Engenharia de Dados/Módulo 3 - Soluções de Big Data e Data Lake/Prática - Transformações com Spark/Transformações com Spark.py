# Prática de Transformações com Spark

# %%
# Importando Spark e criando sessão
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Transformações com Spark').getOrCreate()

spark.version

# %%
# Lendo o README.md do GitHub do Apache/Spark
# https://github.com/apache/spark/blob/master/README.md

linesRdd = spark.sparkContext.textFile('README.md')

linesRdd.count()

# %%
# Mapeando Linha por linha em tupla (linha, num. de chars) - 1 para 1
mapRdd = linesRdd.map(lambda line: (line, len(line)))
mapRdd.collect()

# %%
# Usando flatMap() - Vários para 1
flatMap = linesRdd.flatMap(lambda line: line.split(' '))
flatMap.collect()

# %%
# Filtrando palavras que começam com S
filterRdd = linesRdd.flatMap(lambda line: line.split(' '))\
                    .filter(lambda word: word.lower().startswith('s'))
filterRdd.collect()

# %%
# Criando uma lista e usando o Parallelize
lista = ['um', 'um', 'dois', 'tres', 'tres', 'tres']

rdd = spark.sparkContext.parallelize(lista)
rdd2 = rdd.map(lambda x: (x, 1))\
          .reduceByKey(lambda a, b: a + b)

rdd2.collect()

# %%
# Criando uma lista e usando o parallelize e ordenando pela chave
lista = ['um', 'um', 'dois', 'tres', 'tres', 'tres']

rdd = spark.sparkContext.parallelize(lista)
rdd2 = rdd.map(lambda x: (x, 1))\
          .reduceByKey(lambda a, b: a + b)\
          .sortByKey()

rdd2.collect()

# %%
# Criando uma lista e usando o parallelize e ordenando pelo valor
lista = ['um', 'um', 'dois', 'tres', 'tres', 'tres']

rdd = spark.sparkContext.parallelize(lista)
rdd2 = rdd.map(lambda x: (x, 1))\
          .reduceByKey(lambda a, b: a + b)\
          .sortBy(lambda t: t[1])
# Por padrão é ascendente, caso queira descendente é só acrescentar ', False' após a função lambda

rdd2.collect()

# %%
# %%
# União
lista1 = ['um', 'um', 'dois', 'tres', 'tres', 'tres']
lista2 = ['quatro', 'cinco']

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddUnion = rdd1.union(rdd2)
rddUnion.collect()

# %%
# Intersection
lista1 = ['um', 'um', 'dois', 'tres', 'tres', 'tres']
lista2 = ['um', 'quatro', 'cinco']

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddIntersection = rdd1.intersection(rdd2)
rddIntersection.collect()

# %%
# Distinct
lista1 = ['um', 'um', 'dois', 'tres', 'tres', 'tres']

rdd1 = spark.sparkContext.parallelize(lista1)

rddDistinct = rdd1.distinct()
rddDistinct.collect()

# %%
# Join
lista1 = [('Pedro', 39), ('Maria', 30)]
lista2 = [('Pedro', 'BH'), ('Maria', 'SP'), ('João', 'RJ')]

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddJoin = rdd1.join(rdd2)
rddJoin.collect()

# %%
# Ações
lista1 = [('Pedro', 39), ('Maria', 30)]
lista2 = [('Pedro', 'BH'), ('Maria', 'SP'), ('João', 'RJ')]

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddJoin = rdd1.join(rdd2)
rddJoin
# O Spark não faz nada e executa bastante rápido o código por ser lazy

# %%
# Aqui ele demora a executar porque processa todo o código para exibir na tela
rddJoin.collect()

# %%
rddUnion.take(1)

# %%
# Exemplo de Union e Top
lista1 = ['um', 'um', 'dois', 'tres', 'tres', 'tres']
lista2 = ['quatro', 'cinco']

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddUnion = rdd1.union(rdd2)
rddUnion.collect()
rddUnion.top(3)

# Union, Join, Intersection, Distinct são transformações; collect, count e top são exemplos de ações, o que disparam o processamento do Spark.

# %%
# Exemplo de Count
lista1 = ['um', 'um', 'dois', 'tres', 'tres', 'tres']
lista2 = ['quatro', 'cinco']

rdd1 = spark.sparkContext.parallelize(lista1)
rdd2 = spark.sparkContext.parallelize(lista2)

rddUnion = rdd1.union(rdd2)
rddUnion.count()

# %%
# Exemplo com CountByValue
rddUnion.countByValue()
