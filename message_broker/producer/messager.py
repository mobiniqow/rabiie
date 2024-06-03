import json
from datetime import datetime

import pika

from message_broker.message.message import Message


def serialize_object(obj):
    return json.dumps(obj)


def send_broker_message(
    message: Message,
):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="socket_server_queue")
    channel.exchange_declare("socket_server_exchange")
    data = {
        "type": message.type,
        "payload": message.payload,
        "device_id": message.device_id,
    }
    channel.basic_publish(
        exchange="socket_server_exchange",
        routing_key="socket_server_routing_key",
        body=serialize_object(data),
    )
    print("[x] Sent 'Hello World!'")
    connection.close()
