# Prática do Apache Flink com Apache Kafka
# É necessário para o código a instalação das bibliotecas
# faker, confluent_kafka e simplejson
# pip install faker confluent_kafka simplejson


import random
import datetime
import time

from faker import Faker
from confluent_kafka import SerializingProducer
from datetime import datetime
import json

fake = Faker()

def generate_sales_transaction():
    user = fake.simple_profile()

    return {
        'transactionId': fake.uuid4(),
        'productId': random.choice(['product 1', 'product 2', 'product 3', 'product 4', 'product 5', 'product 6', 'product 7']),
        'productName': random.choice(['notebook', 'smartphone', 'tablet', 'smartwatch', 'earphone', 'speaker']),
        'productBrand': random.choice(['Samsung', 'Apple', 'Xiaomi', 'Huawei', 'Microsoft', 'Oppo']),
        'productCategory': random.choice(['computer', 'portable', 'wearable', 'smart', 'sound']),
        'productPrice': round(random.uniform(100, 1000), 2),
        'productQuantity': random.randint(1, 10),
        'currency': random.choice(['BRL', 'USD', 'EUR', 'LIB']),
        'customerId': user['username'],
        'transactionDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        'paymentMethod': random.choice(['Credit Card', 'Debit Card', 'Paypal', 'Cash'])
    }

def main():

    topic = 'sales-transactions'
    producer = SerializingProducer({
            'bootstrap.servers':'172.17.0.1:9092'
        })


    while True:

        try:

            transaction = generate_sales_transaction()
            transaction['totalAmount'] = transaction['productPrice'] * transaction['productQuantity']

            producer.produce(
                topic,
                key=transaction['transactionId'],
                value=json.dumps(transaction),
                on_delivery=delivery_report
            )
            producer.poll(0)

            time.sleep(0.5)
        
        except BufferError:
            print('Buffer cheio! Espere alguns instantes.')
            time.sleep(1)

        except Exception as e:
            print(e)


def delivery_report(err, msg):
    if err is not None:
        print(f'Nao foi possivel entregar o payload para a gravacao {msg.key()}: {err}')
    else:
        print(f'Mensagem entregue com sucesso no topico {msg.topic} [{msg.partition()}]')


if __name__ == '__main__':
    main()

# kafka-console-consumer --bootstrap-server 172.17.0.1:9092 \
# --topic sales-transactions \
# --from-beginning
