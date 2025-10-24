# Contando Números com Spark
'''
Contando quantas vezes os números aparecerão no arquivo numbers.txt
'''

'''
# %%
# Colocando esse trecho de código por causa de alguns erros que estavam acontecendo
import os, sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
'''

# %%
# Importando Biblioteca Spark
from pyspark.sql import SparkSession

# %%
# Criando um SparkSession
spark = SparkSession.builder.appName('Engenharia de Dados - Tecnologia de Big Data - Aula 2.2').getOrCreate()

spark.version

# %%
# Lendo o arquivo numbers.txt e exibindo o número de partições
filename = 'numbers/numbers.txt'

linesRdd = spark.read.text(filename).rdd.map(lambda r: r[0])
print(f'Números de partições: {linesRdd.getNumPartitions()}')

# %%
from operator import add

# 1 9 8 10 1 9 2

# =>
# 1 2
# 9 1
# 2 1
# ...

countsRdd = linesRdd.flatMap(lambda line: line.split(' '))\
                    .map(lambda number: (int(number), 1))\
                    .reduceByKey(add)\
                    .sortByKey()

# Pega 100% dos dados do RDD (Resilient Distributed Dataset) original
# Divide cada linha em números separados por espaço
# Cria pares (int(chave), valor) onde a chave é o número e o valor é a contagem de quantas vezes ele aparece no dataset
# Soma os valores para cada número igual, obtendo a contagem de cada número

print('Final')

# %%
# Agora que inicia-se o processamento, o Spark é lazy só computa quando precisa do resultado
output = countsRdd.collect()
for (number, count) in output:
    print(number, count)
