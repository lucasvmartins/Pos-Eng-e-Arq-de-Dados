# Desafio Final - Bootcamp: Engenheiro(a) de Dados

## Desafio Final

### Objetivos

O tema do desafio final é a construção de Pipelines ETL com integração do Kafka com uma database (PostgreSQL) usando Kafka Connect e entrega em datalake com Kafka Connect.
Todos os serviços que compõem o Kafka e o database PostgreSQL que servirá de fonte serão implantados com Docker Compose.

Portanto, vamos desenvolver uma solução prática de Engenharia de Dados que implemente a criação de pipelines ETL utilizando o modelo Bronze, Silver e Gold, processados com Apache Spark SQL API e integrados a um Datalake no Amazon S3 via Kafka Connect.

---

## Enunciado

## 1. Pipeline Bronze (Ingestão Bruta)

### Fonte de Dados

* Consumir os dados brutos de uma URL contendo um arquivo CSV com preços e taxas dos títulos públicos (Tesouro Direto), disponibilizado no portal de dados abertos do Tesouro Nacional (CKAN é o sistema de dados abertos usado).

### Ferramenta

* Spark SQL para carregar os dados e criar uma tabela temporária ou persistente (formato Parquet ou Delta).

### Processamento

* Carregar dados brutos para a camada Bronze, sem transformação além da validação do esquema em um banco de dados (por exemplo, PostgreSQL).

---

## 2. Pipeline Silver (Limpeza e Transformação)

### Fonte de Dados

* Tabela Bronze.

### Ferramenta

* Spark SQL para limpeza e transformações.

### Processamento

* Remover duplicações.
* Tratar dados ausentes (ex.: preencher valores nulos ou descartar registros inválidos).
* Ajustar colunas para um formato consistente (ex.: normalizar nomes).
* Salvar os dados limpos em uma tabela Silver em um banco de dados (por exemplo, PostgreSQL).

---

## 3. Pipeline Gold (Agregação e Enriquecimento)

### Fonte de Dados

* Tabela Silver.

### Ferramenta

* Spark SQL para realizar agregações e cálculos.

### Processamento

* Gerar métricas agregadas (ex.: número de usuários ativos, média de idade).
* Criar a camada Gold contendo dados prontos para consumo analítico em um banco de dados (por exemplo, PostgreSQL).

---

# PARTE 01 – CAMADAS BRONZE

## Passo a Passo para Execução

---

## 1. Pré-requisitos

* Docker
* Docker Compose
* Uma conta AWS Free Tier

---

## 2. Configurar o arquivo `.env_kafka_connect`

Edite o arquivo `.env_kafka_connect` com suas chaves AWS como variáveis de ambiente.
Exemplo:

```
AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Lembre-se que o mesmo usuário que possui essa chave precisa ter em suas permissões a permissão `AmazonS3FullAccess` para poder gerenciar os Buckets do S3.

---

## Configurar o Bucket no Amazon S3

O Kafka Connect precisa das credenciais para se autenticar no Amazon S3. Essas credenciais foram fornecidas dentro de arquivo de conguração.

Vá ao console da AWS e crie os buckets com os nomes que preferir, por exemplo:

* `my-bucket-xx-01`
* `my-bucket-xx-02`

Escolha a região compatível:

* `us-east-1`

Ajuste os arquivos de configuração `connect_s3_sink_ipca.config` e `connect_s3_sink_pre.config` em `.../connectors/sink`, substituindo os nomes dos buckets nas linhas:

```
"s3.bucket.name": "my-bucket-xx-0x",
"s3.region": "us-east-1",
```

  ---

## 3. Build da imagem do Kafka Connect

Após clonar o repositório, entre na pasta `./custom-kafka-connectors-image` pelo console e execute:

```
docker buildx build . -t connect-custom:1.0.0
```

Uma nova imagem com o nome `connect-custom` e tag `1.0.0` será criada. Essa é a imagem que nosso serviço connect dentro do `docker-compose.yaml` irá utilizar, com os conectores que precisaremos instalados.

**Explicação:** O comando `docker buildx build` cria uma nova imagem Docker a partir do `Dockerfile` dentro da pasta `./custom-kafka-connectors-image`. Essa pasta contém os arquivos necessários para personalizar a imagem, como congurações especícas e conectores adicionais.

Essa imagem será usada pelo serviço Kafka Connect definido no arquivo `docker-compose.yaml`. Os conectores personalizados incluídos na imagem são necessários para realizar a integração com as fontes de dados **(PostgreSQL)** e destinos **(Amazon S3)**.


---

## 4. Subir o PostgreSQL

Dentro da pasta `./postgres`, execute o arquivo `docker-compose.yaml` rode:

```
docker compose up -d
```

_Obs.: Possa ser que algum serviço postgres já esteja rodando na sua máquina, isso impede que o Docker inicie o contêiner postgres. Caso isso aconteça, verifique os serviços que estão rodando e veja se o postgres já está em execução, se já estiver, pare a execução e execute o docker compose novamente._

---

## 5. Processar o ETL

Abra e execute o arquivo `importar.ipynb` _(não funciona em Colab por causa da conexão local com PostgreSQL)_. Você pode rodar este notebook no **Jupyter** ou **VS Code** com extensão **Jupyter**. Pelo fato do seu Postgres estar em um container local, o código vai dar erro na conexão caso você use o **Google Colab**.

Depois de rodar, confira as tabelas no Postgres. Por exemplo, pode usar o **DBeaver** ou o **pgAdmin 4** como ferramenta gerenciadora do banco de dados.
Os parâmetros de conexão estão dentro do arquivo `docker-compose.yaml` na pasta `./postgres`.

```
postgres:
    image: postgres:13.2
    ports:
      - 5432:5432
    hostname: postgres
    container_name: postgres
    environment: 
      POSTGRES_PASSWORD: postgres
```

---

## 6. Subir a plataforma Confluent com Docker Compose

No arquivo `docker-compose.yaml` localizado na raiz do projeto estamos subindo toda a estrutura da plataforma Confluent. Para isso, vamos entrar na pasta e subir a estrutura.

Na raiz do projeto, rode:

```
docker compose up -d
```

Este Docker Compose cria uma arquitetura Kafka com suporte para:

* Streaming de dados com Kafka Broker
* Coordenação através do Zookeeper
* Gerenciamento de esquemas com Schema Registry
* Integração com sistemas externos via Kafka Connect
* Consultas SQL em tempo real com ksqldb-server e ksqldb-cli
* Interface REST para Kafka via REST Proxy

Se o container do proxy não subir na porta 8082, você pode identificar qual processo está usando a porta 8082 a partir do terminal rodando o comando no Windows `netstat -ano | ndstr :8082`. Você verá o PID (Process ID) do processo que está usando a porta. Obs: para finalizar a tarefa, entre no terminal com acesso de admistrador e execute `taskkill /PID <PID> /F`. Após ter finalizado o processo, tente iniciar o contêiner novamente.

---

## 7. Criar dois tópicos no Kafka

Antes de criar os tópicos, você precisa acessar o contêiner onde o Kafka está rodando. Certique-se de que o Docker está ativo e os serviços do Kafka estão em execução.

Acesse o container do broker:

```
docker exec -it broker bash
```

Após executar esse comando, você estará no terminal do contêiner Kafka Broker.

**Explicação:**
* **docker exec**: Executa um comando em um contêiner ativo.
* **-it**: Abre uma sessão interativa com o contêiner.
* **broker**: Nome do contêiner que roda o Kafka Broker (esse nome pode variar de acordo com a conguração do seu docker-compose.yaml)
* **bash**: Usando a linha de comando

Crie os tópicos no Kafka:

Agora que você está dentro do contêiner do Kafka, use o comando kafka-topics para criar os tópicos. Cada tópico armazenará os dados movidos do PostgreSQL.

### IPCA (Comando para criar o tópico postgres-dadostesouroipca)

```
kafka-topics --create \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1 \
--topic postgres-dadostesouroipca
```

### PRE (Comando para criar o tópico postgres-dadostesouropre)

```
kafka-topics --create \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1 \
--topic postgres-dadostesouropre
```

* **--bootstrap-server localhost:9092:** Especifica o endereço do servidor Kafka. O localhost:9092 é o endereço padrão usado em contêineres Kafka.
* **--partitions 1:** Define o número de partições do tópico. Para este exemplo, usamos 1 partição.
* **--replication-factor 1:** Define o número de réplicas para o tópico. Usamos 1, pois estamos rodando o Kafka em um único broker.
* **--topic postgres-dadostesouro...:** Nome do tópico sendo criado.

### Verificar se os tópicos foram criados:

Após executar os comandos acima, é importante confirmar que os tópicos foram criados com sucesso. Use o comando abaixo para listar os tópicos disponíveis no Kafka:

```
kafka-topics --bootstrap-server localhost:9092 --list
```

Isso exibirá todos os tópicos criados no Kafka. Você deve ver os nomes `postgres-dadostesouroipca` e `postgres-dadostesouropre` na lista.

---

## 8. Registrar os Connectors Kafka Source

Os conectores Kafka Source serão configurados para extrair dados do PostgreSQL e enviá-los para os tópicos no Kafka. Para isso, vamos precisar de um arquivo no formato json contendo as configurações do conector que vamos registrar. O arquivo `connect_jdbc_postgres_ipca.config` possui a implementação do **IPCA**. O arquivo `connect_jdbc_postgres_pre.config` possui a implementação do **PRE**.

Os conectores são configurados através de arquivos JSON contendo os parâmetros necessários. Aqui está como configurar:

Crie os arquivos com o seguinte conteúdo e salve cada arquivo no diretório onde você irá executar os comandos de registro (./connectors/source):

### `connect_jdbc_postgres_ipca.config`

```json
{
    "name": "postg-connector-ipca",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "tasks.max": 1,
        "connection.url": "jdbc:postgresql://postgres:5432/postgres",
        "connection.user": "postgres",
        "connection.password": "postgres",
        "mode": "timestamp",
        "timestamp.column.name": "dt_update",
        "table.whitelist": "public.dadostesouroipca",
        "topic.prefix": "postgres-",
        "validate.non.null": "false",
        "poll.interval.ms": 500
    }
}
```

### `connect_jdbc_postgres_pre.config`

```json
{
    "name": "postg-connector",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "tasks.max": 1,
        "connection.url": "jdbc:postgresql://postgres:5432/postgres",
        "connection.user": "postgres",
        "connection.password": "postgres",
        "mode": "timestamp",
        "timestamp.column.name": "dt_update",
        "table.whitelist": "public.dadostesouropre",
        "topic.prefix": "postgres-",
        "validate.non.null": "false",
        "poll.interval.ms": 500
    }
}
```

### Execute os comandos curl para registrar os conectores:

Esta etapa envolve o registro de conectores no Kafka Connect utilizando o comando curl no terminal. O Kafka Connect é uma ferramenta usada para integrar sistemas externos com o Apache Kafka, e, neste caso, estamos registrando conectores JDBC para conectar bancos de dados **PostgreSQL** ao Kafka. O objetivo é registrar dois conectores JDBC no Kafka Connect para que ele possa ler dados de duas tabelas do **PostgreSQL** (provavelmente relacionadas ao IPCA e Pre-fixados, conforme os arquivos de configuração).

No terminal do host **(não dentro do contêiner)**, execute os comandos para registrar os conectores. Certifique-se de estar no diretório onde os arquivos estão salvos ou forneça o caminho completo _(por exemplo, .../connectors/source/)_, antes de executar o comando.

### Registrar:

```
curl -X POST -H "Content-Type: application/json" --data @connect_jdbc_postgres_ipca.config http://localhost:8083/connectors
```
```
curl -X POST -H "Content-Type: application/json" --data @connect_jdbc_postgres_pre.config http://localhost:8083/connectors
```

---

## Vericar os conectores e tópicos

Verifique o consumo de dados nos tópicos. O comando kafka-console-consumer é usado para consumir mensagens de um tópico Kafka. Vamos verificar os dados nos tópicos `postgres-dadostesouroipca` e `postgres-dadostesouropre`.

### Explicação do comando:

* **kafka-console-consumer:**
  * Ferramenta CLI do Kafka para consumir mensagens de um tópico
* **--bootstrap-server localhost:9092:**
  * Especifica o servidor Kafka que será usado para consumir mensagens
  * No exemplo, usamos localhost:9092, que é a porta padrão do Kafka Broker
* **--topic <nome_do_tópico>:**
  * Define o tópico Kafka de onde você quer consumir as mensagens
  * No seu caso, os tópicos são `postgres-dadostesouroipca` e `postgres-dadostesouropre`.
* **--from-beginning:**
  * Indica que o consumo de mensagens deve começar desde o início do tópico _(todas as mensagens enviadas desde a criação do tópico)_.

Vamos entrar no Kafka Broker que está rodando:

```
docker exec -it broker bash
```

### Verifique o consumo de dados nos tópicos:

### IPCA

```
kafka-console-consumer --bootstrap-server localhost:9092 \
--topic postgres-dadostesouroipca \
--from-beginning
```

### PRE

```
kafka-console-consumer --bootstrap-server localhost:9092 \
--topic postgres-dadostesouropre \
--from-beginning
```

---

## 9. Configurar os Sink Connectors

Exemplos:

### `connect_s3_sink_ipca.config`

```json
{
  "name": "s3-sink-ipca",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "keys.format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
    "flush.size": 2,
    "schema.compatibility": "FULL",
    "s3.bucket.name": "NOME-DO-BUCKET",
    "s3.region": "us-east-1",
    "s3.object.tagging": true,
    "s3.ssea.name": "AES256",
    "topics.dir": "raw-data/kafka",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "tasks.max": 1,
    "topics": "postgres-dadostesouroipca"
  }
}
```

---

## 10. Verificar entrega no S3

Os arquivos devem aparecer no bucket em formato JSON, por exemplo:

```json
{
  "CompraManha": 12.73,
  "VendaManha": 12.79,
  "PUCompraManha": 631.4,
  "PUVendaManha": 630.11,
  "PUBaseManha": 629.81,
  "Data_Vencimento": 1420070400000,
  "Data_Base": 1298851200000,
  "Tipo": "PRE-FIXADOS",
  "dt_update": 1734381830665
}
```

---

# PARTE 02 – CAMADAS SILVER E GOLD

## 1. Configuração de Permissões nos Buckets

Inclua permissões similares a:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowWriteAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/ricardobalves"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket-ric-01",
        "arn:aws:s3:::my-bucket-ric-01/*"
      ]
    }
  ]
}
```

---

# 2. Instalação do Apache Spark

Pode ser:

### a) Instalação local (Spark + Hadoop)

ou

### b) Uso via contêineres Docker

(Conteúdo mantido como no original, apenas corrigido.)

---

# 3. Notebook `etl-spark.ipynb`

Trechos corrigidos, incluindo:

### Bronze → Silver

```python
df_silver = df_bronze.dropDuplicates()

df_silver = df_silver.withColumn("Data_Vencimento",
    from_unixtime(col("Data_Vencimento") / 1000, "yyyy-MM-dd")) \
    .withColumn("Data_Base",
    from_unixtime(col("Data_Base") / 1000, "yyyy-MM-dd")) \
    .withColumn("dt_update",
    from_unixtime(col("dt_update") / 1000, "yyyy-MM-dd HH:mm:ss"))

df_silver = df_silver.fillna({
    "PUCompraManha": 0,
    "PUVendaManha": 0,
    "PUBaseManha": 0
})
```

### Silver → Gold

```python
df_gold = df_silver.groupBy("Tipo").agg(
    avg("PUCompraManha").alias("Media_PUCompraManha"),
    avg("PUVendaManha").alias("Media_PUVendaManha"),
    count("*").alias("Total_Registros")
)
```

---

## 4. Validar Resultados no S3

* `processed-data/ipca/silver/`: dados limpos
* `analytics/ipca/gold/`: dados agregados

---

Se quiser, posso também:

✅ Criar um **PDF formatado**
✅ Criar uma **versão resumida para entrega**
✅ Criar um **guia passo a passo simplificado**

É só pedir!
