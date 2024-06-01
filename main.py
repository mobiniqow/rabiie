import json
import os
import pika
import django
from message_broker.messager import send_broker_message

os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings.dev"

django.setup()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/',
                                                               pika.PlainCredentials('guest', 'guest')))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='backend_queue')
channel.exchange_declare(exchange='backend_exchange')

send_broker_message(",asdasd", "salam agha mobin")


def callback(ch, method, properties, body):
    a=json.loads(body)
    # print(f"aa {bytearray.fromhex( a['payload'])}")
    print(f"data  {a}")
    print(f"payload {bytes(a['payload'], encoding='utf8') }")
    print(f"type {a['type']}")
    print(f"deviceId {a['deviceId']}")

    #todo
    # ch.basic_ack(delivery_tag=method.delivery_tag)


channel.queue_bind(queue='backend_queue', exchange='backend_exchange', routing_key="backend_routing_key")
channel.basic_consume(queue='backend_queue', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
