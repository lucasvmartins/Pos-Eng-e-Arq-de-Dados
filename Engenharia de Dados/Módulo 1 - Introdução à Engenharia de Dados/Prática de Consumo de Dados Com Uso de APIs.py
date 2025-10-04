# 1- Baixar os dados do Novo Bolsa Família dos meses 01/2024 e 03/
#    2024 pela API

# 2- Filtrar os dados pelo município de Araçoiaba e verificar 
#    no mês de 01/2024 quanto o município recebeu

# 3- Contar quantos benefícios foram recebidos por cada UF e qual 
#    a UF que mais recebeu benefício em 03/2024

# %%
#! pip install requests # Caso precise instalar o requests

# %%
import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO

# %%
# Envia uma requisição para baixar o arquivo
def baixar_dados(url):

    # Envia a requisição para baixar os dados
    response = requests.get(url)

    # Checa se a requisição foi respondida com êxito
    if response.status_code == 200:

        # Usa o BytesIO para ler o arquivo ZIP da memória
        arquivo_zip = ZipFile(BytesIO(response.content))

        # Extrai o nome dos arquivos dentro do ZIP
        nomes_dos_arquivos = arquivo_zip.namelist()

        # Assume que há somente um arquivo CSV e o extrai
        with arquivo_zip.open(nomes_dos_arquivos[0]) as arquivo_csv:

            # Lê o CSV para um DataFrame
            df = pd.read_csv(arquivo_csv, sep=';', encoding='ISO-8859-1')

            return df
    
    else:
        print("Não foi possível baixar o arquivo. Código de erro:", response.status_code)
        return None

# %%
# URL da API dos dados de 01/2024
url = 'https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia/202401'

# %%
# Baixando os dados
dataframe = baixar_dados(url)


# %%
# Estrutura do dataframe
dataframe.head()
dataframe.describe()

# %%
# Filtrar pelo município
df_filtrado_municipio = dataframe[dataframe['NOME MUNICÍPIO'] == 'ARACOIABA']
df_filtrado_municipio

# %%
# Tratamento do campo 'Valor da Parcela'
valor_parcela_tratado = df_filtrado_municipio['VALOR PARCELA'].str.replace(',', '.').astype(float)
valor_parcela_tratado

# %%
# Soma de quantidade de parcelas
soma_qtd_parcelas = valor_parcela_tratado.sum()
soma_qtd_parcelas

# %%
# URL da API dos dados de 03/2024
url = 'https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia/202403'

dataframe = baixar_dados(url)

# %%
# Filtrar dados por 'UF'
df_filtrado_uf = dataframe['UF']
df_filtrado_uf

# %%
# Frequencia de UFs
frequencia_uf = df_filtrado_uf.value_counts()
frequencia_uf

# %%
# UF com mais recebimentos
uf_mais_frequente = frequencia_uf.max()
uf_mais_frequente
