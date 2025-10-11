# Exemplo de Zero ETL Approach com Astronomer.io

from datetime import datetime

# pip install apache-airflow
from airflow.models import DAG

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

# Input
S3_FOLDER_PATH = 's3://teste-astro'
S3_FILE_PATH = '/clientes.csv'
S3_CONNECTION_ID = 'aws_astro'

# Output
POSTGRES_CONNECTION_ID = 'postgres_astro'
POSTGRES_TABLE = 'tb_customers'

dag = DAG(
    dag_id = 'pipelineS3Postgres',
    start_date=datetime(2025, 10, 11),
    schedule='@daily'
)

with dag:
    pipeline = aql.load_file(
        input_file = File(path = S3_FOLDER_PATH + S3_FILE_PATH, conn_id = S3_CONNECTION_ID),
        output_file = Table(name = POSTGRES_TABLE, conn_id = POSTGRES_CONNECTION_ID),
        if_exists = 'replace'
    )
