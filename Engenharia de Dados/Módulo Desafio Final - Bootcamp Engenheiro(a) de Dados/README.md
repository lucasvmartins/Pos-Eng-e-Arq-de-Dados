# Desafio Final - Bootcamp Engenharia de Dados: Construção de Pipelines ETL

## Objetivos

O tema do desafio final é a construção de Pipelines ETL com integração do Kafka com uma database (Postgresql) usando Kafka Connect e entrega em datalake com Kafka Connect. Todos os serviços que compõem o Kafka e o database PostgreSQL que servirá de fonte serão implantados com docker compose.

Portanto, vamos desenvolver uma solução prática de Engenharia de Dados que implemente a criação de pipelines ETL utilizando o modelo bronze, silver e gold, processados com Apache Spark SQL API e integrados a um datalake no Amazon S3 via Kafka Connect.


## Requisitos

1. Pipeline Bronze (Ingestão Bruta):
    - Fonte de Dados: Vamos consumir os dados brutos de uma URL contendo um arquivo CSV com preços e taxas dos títulos públicos (Tesouro Direto), disponibilizado no portal de dados abertos o Tesouro Nacional (CKAN é o sistema de dados abertos usado).
    - Ferramenta: Spark SQL para carregar os dados e criar uma tabela temporária ou persistente (formato Parquet ou Delta).
    - Processamento: o Carregar dados brutos para a camada Bronze, sem transformação além da validação do esquema em um banco de dados (por exemplo, PostgreSQL).

3. Pipeline Silver (Limpeza e Transformação):
    - Fonte de Dados: Tabela Bronze.
    - Ferramenta: Spark SQL para limpeza e transformações.
    - Processamento:
      - Remover duplicações.
      - Tratar dados ausentes (ex.: preencher valores nulos ou descartar registros inválidos).
      - Ajustar colunas para um formato consistente (ex.: normalizar nomes).
      - Salvar os dados limpos em uma tabela Silver em um banco de dados (por exemplo, PostgreSQL).

4. Pipeline Gold (Agregação e Enriquecimento):
    - Fonte de Dados: Tabela Silver.
    - Ferramenta: Spark SQL para realizar agregações e cálculos.
    - Processamento:
      - Gerar métricas agregadas (ex.: número de usuários ativos, média de idade).
      - Criar a camada Gold contendo dados prontos para consumo analítico em um banco de dados (por exemplo, PostgreSQL).


---

## PARTE 01 – CAMADA BRONZE

