# Exemplos de códigos com tipos de dados

# %%

nome = "Lucas Martins"
print(nome, type(nome))

# %%

idade = '45'
idade = int(15)
print(idade, type(idade))

# %%

idade = 35
type(idade)

# %%

altura = '1,63'
type(altura)

# %%
num_altura = float(altura.replace(',', '.'))

print(altura, type(altura))
print(num_altura, type(num_altura))

# %%

booleano = 'true'
booleano_new = bool(booleano)

print('booleano:', booleano,'\n', type(booleano))
print('booleano_new:', booleano_new,'\n', type(booleano_new))

# %%

booleano2 = True
print(type(booleano2))

# %%

data = '2025-09-30'
type(data)

# %%
from datetime import datetime, date

# %%

data_parse = datetime.strptime(data, '%Y-%m-%d').date() # String parse time
print(data_parse, '\n', type(data_parse))

# %%

lista = ['Lucas', 29, 1.63, True]
print(lista[3], type(lista[3]))

# %%

dicionario = dict(nome = 'Lucas', idade = 29)
dicionario

dicionario['nome']
