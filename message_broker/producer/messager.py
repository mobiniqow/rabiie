import json
from datetime import datetime

import pika


def serialize_object(obj):
    return json.dumps(obj)


def send_broker_message(device_id, message, ):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='socket_server_queue')
    channel.exchange_declare('socket_server_exchange')
    data = {
        "message": message,
        "device_id": device_id,
        "payload": device_id,
        "type": device_id,
        "date": str(datetime.now())
    }
    channel.basic_publish(exchange='socket_server_exchange', routing_key='socket_server_routing_key',
                          body=serialize_object(data))
    print("[x] Sent 'Hello World!'")
    connection.close()

