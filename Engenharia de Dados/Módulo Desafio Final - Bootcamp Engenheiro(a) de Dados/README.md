1. Pipeline Bronze (Ingestão Bruta)
● Fonte de Dados: Vamos consumir os dados brutos de uma URL contendo um
arquivo CSV com preços e taxas dos títulos públicos (Tesouro Direto),
disponibilizado no portal de dados abertos do Tesouro Nacional (CKAN é o
sistema de dados abertos usado).
● Ferramenta: Spark SQL para carregar os dados e criar uma tabela temporária ou
persistente (formato Parquet ou Delta).
● Processamento:
o Carregar dados brutos para a camada Bronze, sem transformação além da
validação do esquema em um banco de dados (por exemplo, PostgreSQL).
2. Pipeline Silver (Limpeza e Transformação)
● Fonte de Dados: Tabela Bronze.
1
● Ferramenta: Spark SQL para limpeza e transformações.
● Processamento:
o Remover duplicações.
o Tratar dados ausentes (ex.: preencher valores nulos ou descartar registros
inválidos).
o Ajustar colunas para um formato consistente (ex.: normalizar nomes).
o Salvar os dados limpos em uma tabela Silver em um banco de dados (por
exemplo, PostgreSQL).
3. Pipeline Gold (Agregação e Enriquecimento)
● Fonte de Dados: Tabela Silver.
● Ferramenta: Spark SQL para realizar agregações e cálculos.
● Processamento:
o Gerar métricas agregadas (ex.: número de usuários ativos, média de
idade).
o Criar a camada Gold contendo dados prontos para consumo analítico em
um banco de dados (por exemplo, PostgreSQL).







# Desafio Final - Bootcamp Engenharia de Dados: Construção de Pipelines ETL

O tema do desao nal é a construção de Pipelines ETL com integração do Kafka com uma database (postgresql) usando kafka connect e entrega em data lake com kafka connect. Todos os serviços que compõem o kafka e o database PostgreSQL que servirá de fonte serão implantados com docker-compose.

Portanto, vamos desenvolver uma solução prática de Engenharia de Dados que implemente a criação de pipelines ETL utilizando o modelo bronze, silver e gold, processados com Apache Spark SQL API e integrados a um datalake no Amazon S3 via Kafka Connect.

---

# Passo a passo para execução

## 1 - Pré-requisitos

- Docker
- docker-compose
- pgAdmin 4 (PostgreSQL)
- Uma conta na AWS
- Python

## 2 - "Buildar" o conector Kafka custom

Com o terminal, entrar na pasta "custom-kafka-connector-image" e executar o seguinte comando:

```

```

## 2 - Subir o ambiente postgres
Com os prerequisitos instalados e testados, baixar o projeto no GitHub e entrar na pasta `Desafio\Flink`, execute o seguinte comando:

```bash
cd docker
docker-compose up -d
```
O ambiente será baixado e provisionado em sua máquina, conforme desenho arquitetural descrito na pasta `arquitetura`.

## 3 - Carregar os dados fakes no Tópico do Kafka

Na pasta `python` executar a geração dos dados com o comando:
```bash
python3 .\main.py
```

## 4 - Pare os dados fake

```bash
CTRL + C
```


## 5 - Criar o arquivo JAR com o Intellij

Abrir o Intellij, abrir a pasta do projeto Java e criar o JAR que será depositado no Flink.
Abra o terminal e digite: 

```bash
mvn clean compile package
```

## 6 - Abrir o Manager do Flink

Vá até seu navegador e digite o seguinte endereço:

```bash
http://localhost:8081
```

- No Intellij, abra a pasta Target (abrir com o explorer) e copie o JAR em seu Desktop (normalmente: FlinkCommerce-2.0-SNAPSHOT.jar).
- Depois clique no menu lateral esquerdo na opção `Submit new Job`.
- Clique no botão azul `Add new`.
- Selecione o arquivo JAR do desktop.
- Clique sobre o objeto enviado e selecione o botão `Submit`.


## 7 - Verifique se o Job está executando corretamente

Na aba `Jobs \ Running Jobs` verifique se seu Job está apresentando o estado `Azul` (o estado `Vermelho` deve desaparecer em poucos segundos).


## 8 - Gere mais dados pelo Python

Volte ao terminal e execute novamente nosso programa `main.py`

Na pasta `python` executar a geração dos dados com o comando:
```bash
python3 .\main.py
```

## 9 - Valide

Abra o PostgreSQL e verifique se as tabelas `transactions` e `sales_per_category` foram criadas, e se seus dados foram recebidos.

---

**Parabéns**!! Você acabou de concluir o seu pipeline de processamento de dados em tempo real usando a plataforma Flink no docker-compose!