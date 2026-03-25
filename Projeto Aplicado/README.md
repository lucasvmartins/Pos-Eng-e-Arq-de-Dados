# Projeto Aplicado - Especialização em Engenharia e Arquitetura de Dados

## Arquitetura de Pipeline de Dados Financeiros em Nuvem com Mensageria e Dashboard Analítico em Tempo Quase Real

**Autor:** Lucas Vieira Martins  
**Orientadora:** Daniella Pimenta Brito Alves  
**Instituição:** XP Educação — Faculdade XPe  
**Data:** Fevereiro de 2026

---

## Objetivo

Desenvolver e implementar uma solução para extração e persistência de dados financeiros em ambiente local, com a construção de um pipeline de fluxo contínuo de dados com fila de mensageria para migração e armazenamento em nuvem, possibilitando a visualização de informações como cotações de moedas, criptomoedas, índice de volatilidade e principais bolsas de valores por meio de um dashboard online, garantindo acesso remoto, centralizado e confiável para apoiar a tomada de decisão estratégica do investidor.

---

## Arquitetura da Solução

```
yfinance API
     │
     ▼
Python Script (coleta a cada 5s)
     │
     ▼
PostgreSQL (Docker) ──► Kafka Connect (Source - JDBC)
                                  │
                                  ▼
                           Kafka Broker (Tópico: postgres-financial)
                                  │
                                  ▼
                        Kafka Connect (Sink - S3)
                                  │
                                  ▼
                           Amazon S3 (JSON)
                                  │
                                  ▼
                           Amazon Athena (SQL)
                                  │
                                  ▼
                          Grafana Cloud (Dashboard)
```

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Extração de Dados | Python + yfinance |
| Banco Local | PostgreSQL 13.2 (Docker) |
| Mensageria | Apache Kafka (Confluent 7.0.0) |
| Orquestração de Contêineres | Docker / Docker Compose |
| Armazenamento em Nuvem | Amazon S3 |
| Consulta Analítica | Amazon Athena |
| Visualização | Grafana Cloud |

---

## Dados Coletados

| Indicador | Ticker |
|---|---|
| IBOVESPA | `^BVSP` |
| S&P 500 | `^GSPC` |
| Dow Jones | `^DJI` |
| USD/BRL | `BRL=X` |
| EUR/BRL | `EURBRL=X` |
| GBP/BRL | `GBPBRL=X` |
| JPY/BRL | `JPYBRL=X` |
| Bitcoin | `BTC-USD` |
| Ethereum | `ETH-USD` |
| VIX | `^VIX` |
| VIX BR | `^VXEWZ` |

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.x com as bibliotecas `yfinance` e `psycopg2`
- Conta AWS (Free Tier é suficiente)
- Conta Grafana Cloud (plano gratuito é suficiente, se não tiver, o uso gera gastos de centavos de dólares)
- Chave de acesso AWS (Access Key ID + Secret Access Key) com permissões de S3 e Athena

---

## Sprint 1 — Infraestrutura Local e Coleta de Dados

### 1. Configurar o arquivo `.env_kafka_connect`

Edite o arquivo `.env_kafka_connect` com suas chaves AWS:

```
AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

O usuário IAM vinculado a essa chave precisa ter as permissões `AmazonS3FullAccess` e `AmazonAthenaFullAccess`.

---

### 2. Subir o contêiner PostgreSQL

Na pasta **postgres** do projeto, execute o `docker-compose.yaml` do PostgreSQL:

```bash
docker compose up -d
```

Configuração do contêiner:

```yaml
version: '3'
services:
  postgres:
    image: postgres:13.2
    ports:
      - 5432:5432
    hostname: postgres
    container_name: postgres
    environment:
      POSTGRES_PASSWORD: postgres
    networks:
      - proxynet
    volumes:
      - "/etc/timezone:/etc/timezone:ro"
      - "/etc/localtime:/etc/localtime:ro"

networks:
  proxynet:
    name: custom_network
```

---

### 3. Criar a tabela no PostgreSQL

Conecte-se ao banco e execute o script SQL abaixo para criar a tabela que receberá os dados:

```sql
CREATE TABLE financial (
    data_hora  TIMESTAMP PRIMARY KEY,
    IBOVESPA   DOUBLE PRECISION,
    SP500      DOUBLE PRECISION,
    DOWJONES   DOUBLE PRECISION,
    USD_BRL    DOUBLE PRECISION,
    EUR_BRL    DOUBLE PRECISION,
    GBP_BRL    DOUBLE PRECISION,
    JPY_BRL    DOUBLE PRECISION,
    BITCOIN    DOUBLE PRECISION,
    ETHEREUM   DOUBLE PRECISION,
    VIX        DOUBLE PRECISION,
    VIX_BR     DOUBLE PRECISION
);
```

> **Atenção:** Use `DOUBLE PRECISION` e não `NUMERIC`. Campos do tipo `NUMERIC` são serializados pelo Kafka Connect e codificados em Base64 ao serem enviados como JSON, tornando os valores ilegíveis.

---

### 4. Executar o script de coleta de dados

O script Python coleta os dados a cada 5 segundos via biblioteca `yfinance` e os persiste no banco local.

**Obtenção dos dados:**

```python
import yfinance as yf
from datetime import datetime

TICKERS = {
    "IBOVESPA": "^BVSP",
    "SP500": "^GSPC",
    "DOWJONES": "^DJI",
    "USD_BRL": "BRL=X",
    "EUR_BRL": "EURBRL=X",
    "GBP_BRL": "GBPBRL=X",
    "JPY_BRL": "JPYBRL=X",
    "BITCOIN": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "VIX": "^VIX",
    "VIX_BR": "^VXEWZ"
}

def get_data():
    snapshot = {}
    now = datetime.now()
    snapshot["data_hora"] = now
    for ativo, ticker in TICKERS.items():
        hist = yf.Ticker(ticker).history(period="1d", interval="1m")
        snapshot[ativo] = (
            float(hist.iloc[-1]["Close"])
            if not hist.empty
            else None
        )
    return snapshot
```

**Persistência no banco:**

```python
import psycopg2
import time

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

while True:
    try:
        data = get_data()
        cursor.execute(
            """
            INSERT INTO financial (
                data_hora, IBOVESPA, SP500, DOWJONES,
                USD_BRL, EUR_BRL, GBP_BRL, JPY_BRL,
                BITCOIN, ETHEREUM, VIX, VIX_BR
            )
            VALUES (
                %(data_hora)s, %(IBOVESPA)s, %(SP500)s, %(DOWJONES)s,
                %(USD_BRL)s, %(EUR_BRL)s, %(GBP_BRL)s, %(JPY_BRL)s,
                %(BITCOIN)s, %(ETHEREUM)s, %(VIX)s, %(VIX_BR)s
            )
            """,
            data
        )
        conn.commit()
        print(f"Snapshot inserido em {data['data_hora']}")
        time.sleep(5)
    except Exception as e:
        conn.rollback()
        print("Erro:", e)
        time.sleep(5)
```

---

## Sprint 2 — Mensageria com Kafka e Migração para o S3

### 1. Criar o Bucket S3

Acesse o console da AWS e crie um bucket, por exemplo:

- `seu-bucket`

Escolha a região `us-east-1`.

> **Atenção:** Cuidado com a região, sempre usaremos a `us-east-1`.

---

### 2. Build da imagem customizada do Kafka Connect

A imagem customizada inclui os conectores JDBC (PostgreSQL) e S3 já instalados.

**Dockerfile:**

```dockerfile
FROM confluentinc/cp-kafka-connect-base:7.0.0

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.4.1 \
    && confluent-hub install --no-prompt confluentinc/kafka-connect-s3:10.0.7
```

**Para _buildar_ o Dockerfile, é preciso entrar na pasta `custom-kafka-connector-image` e executar o comando:**

```bash
docker buildx build . -t connect-custom:1.0.0
```

---

### 3. Subir o cluster Kafka com Docker Compose

Na raiz do projeto, execute:

```bash
docker compose up -d
```

O Docker Compose sobe toda a estrutura da plataforma Confluent com os seguintes serviços: `zookeeper`, `broker`, `schema-registry`, `rest-proxy`, `connect`, `ksqldb-server` e `ksqldb-cli`.

---

### 4. Criar o tópico Kafka

Acesse o broker:

```bash
docker exec -it broker bash
```

Dentro do broker, crie o tópico:

```bash
kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1 \
  --topic postgres-financial
```

Verifique se o tópico foi criado:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

---

### 5. Configurar e registrar os conectores

**Source Connector** — lê os dados do PostgreSQL e os publica no tópico Kafka.

Arquivo `connect_jdbc_postgres_financial.config`:

```json
{
    "name": "postg-connector-financial",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "tasks.max": 1,
        "connection.url": "jdbc:postgresql://postgres:5432/postgres",
        "connection.user": "postgres",
        "connection.password": "postgres",
        "mode": "timestamp",
        "timestamp.column.name": "data_hora",
        "table.whitelist": "public.financial",
        "topic.prefix": "postgres-",
        "validate.non.null": "false",
        "poll.interval.ms": 500
    }
}
```

**Sink Connector** — consome o tópico Kafka e entrega os dados no S3.

Arquivo `connect_s3_sink_financial.config`:

```json
{
    "name": "s3-sink-financial",
    "config": {
        "connector.class": "io.confluent.connect.s3.S3SinkConnector",
        "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
        "keys.format.class": "io.confluent.connect.s3.format.json.JsonFormat",
        "schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
        "flush.size": 2,
        "schema.compatibility": "FULL",
        "s3.bucket.name": "seu-bucket",
        "s3.region": "us-east-1",
        "s3.object.tagging": true,
        "s3.ssea.name": "AES256",
        "topics.dir": "raw-data/kafka/financial",
        "storage.class": "io.confluent.connect.s3.storage.S3Storage",
        "tasks.max": 1,
        "topics": "postgres-financial"
    }
}
```

**Registre os conectores** (fora do contêiner, no diretório dos arquivos de configuração):

```bash
curl -X POST -H "Content-Type: application/json" --data \
  @connect_jdbc_postgres_financial.config http://localhost:8083/connectors
```

```bash
curl -X POST -H "Content-Type: application/json" --data \
  @connect_s3_sink_financial.config http://localhost:8083/connectors
```

---

### 6. Verificar os dados no S3

Os dados devem chegar ao bucket no seguinte formato JSON:

```json
{
    "data_hora": 1769626225670,
    "ibovespa": 183445.734375,
    "sp500": 6976.27978515625,
    "dowjones": 49010.23046875,
    "usd_brl": 5.193900108337402,
    "eur_brl": 6.205999851226807,
    "gbp_brl": 7.171500205993652,
    "jpy_brl": 0.033730000257492065,
    "bitcoin": 89271.3984375,
    "ethereum": 3014.89111328125,
    "vix": 16.3799991607666,
    "vix_br": 32.66999816894531
}
```

---

## Sprint 3 — Amazon Athena e Dashboard no Grafana Cloud

### 1. Criar banco de dados e tabela no Athena

Crie também um diretório dentro do bucket S3 para receber os resultados de saída do Athena, por exemplo `athena-results/`.

No editor de consultas do Athena, execute:

```sql
CREATE DATABASE IF NOT EXISTS financial_db;
```

Em seguida, crie a tabela externa apontando para os arquivos JSON no S3:

```sql
CREATE EXTERNAL TABLE financial_data (
    data_hora BIGINT,
    ibovespa  DOUBLE,
    sp500     DOUBLE,
    dowjones  DOUBLE,
    usd_brl   DOUBLE,
    eur_brl   DOUBLE,
    gbp_brl   DOUBLE,
    jpy_brl   DOUBLE,
    bitcoin   DOUBLE,
    ethereum  DOUBLE,
    vix       DOUBLE,
    vix_br    DOUBLE
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://seu-bucket/raw-data/kafka/financial/postgres-financial/partition=0/';
```

Para converter o campo de timestamp e visualizar os dados:

```sql
SELECT
    from_unixtime(data_hora / 1000) AS time,
    ibovespa,
    sp500,
    bitcoin
FROM financial_data
ORDER BY time DESC
LIMIT 50;
```

---

### 2. Permissões IAM

O usuário IAM precisa das seguintes políticas para operar corretamente:

- `AmazonS3FullAccess`
- `AmazonAthenaFullAccess`
- `AWSBillingConductorFullAccess`
- `AWSBillingConductorReadOnlyAccess`
- `AWSBillingReadOnlyAccess`

---

### 3. Criar conta no Grafana Cloud

Acesse [grafana.com](https://grafana.com) e crie uma conta gratuita. O plano gratuito é suficiente para este projeto.

---

### 4. Conectar o Grafana ao Athena

Em **Connections > Data sources**, adicione uma nova fonte do tipo **Amazon Athena** e preencha:

- **Authentication Provider:** Access & secret key
- **Access Key ID:** sua chave de acesso AWS
- **Secret Access Key:** sua chave secreta AWS
- **Default Region:** `us-east-1`
- **Database:** `financial`
- **Workgroup / S3 output location:** caminho do bucket de resultados (`s3://seu-bucket/athena-results/`)

---

### 5. Criar os dashboards no Grafana

No Grafana, crie um novo Dashboard e adicione um painel para cada categoria de ativo, utilizando as queries SQL abaixo.

**Bolsas de Valores:**

```sql
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'IBOVESPA' AS asset, ibovespa AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'SP500' AS asset, sp500 AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'DOWJONES' AS asset, dowjones AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
ORDER BY time
```

**Moedas:**

```sql
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'USD/BRL' AS asset, usd_brl AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'EUR/BRL' AS asset, eur_brl AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'GBP/BRL' AS asset, gbp_brl AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'JPY/BRL' AS asset, jpy_brl AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
ORDER BY time
```

**Criptomoedas:**

```sql
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'BITCOIN' AS asset, bitcoin AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'ETHEREUM' AS asset, ethereum AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
ORDER BY time
```

**Índices de Volatilidade:**

```sql
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'VIX' AS asset, vix AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
UNION ALL
SELECT
    from_unixtime(data_hora / 1000) AS time,
    'VIX_BR' AS asset, vix_br AS value
FROM financial.financial_data
WHERE $__timeFilter(from_unixtime(data_hora / 1000))
ORDER BY time
LIMIT 50;
```

---

## Lições Aprendidas

- A correta modelagem dos tipos de dados é fundamental: campos `NUMERIC` no PostgreSQL são serializados em Base64 pelo Kafka Connect; a solução foi migrar para `DOUBLE PRECISION`.
- O Grafana Cloud não é capaz de unificar múltiplos arquivos JSON distribuídos no S3 diretamente. O Amazon Athena foi necessário como camada intermediária de consulta SQL sobre o data lake.
- A integração entre PostgreSQL, Kafka, S3 e Athena exige atenção especial às permissões IAM para evitar bloqueios de acesso entre os serviços.

---

## Próximos Passos

- Inclusão de novas bolsas de valores internacionais, moedas e criptomoedas
- Melhorias de escalabilidade na arquitetura para maior volume e frequência de dados
- Aprimoramento dos gráficos no Grafana com indicadores técnicos e alertas automáticos
- Desenvolvimento de um site próprio para centralizar a visualização dos dashboards
- Incorporação de modelos de Machine Learning para previsão de tendências

---

## Repositório

Códigos do projeto disponíveis em:  
[github.com/lucasvmartins/Pos-Eng-e-Arq-de-Dados/tree/main/Projeto%20Aplicado](https://github.com/lucasvmartins/Pos-Eng-e-Arq-de-Dados/tree/main/Projeto%20Aplicado)
