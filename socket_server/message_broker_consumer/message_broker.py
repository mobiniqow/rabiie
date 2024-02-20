import json

import pika
import threading

from socket_server.client_manager import ClientManager


class MessageListenerThread(threading.Thread):
    def __init__(self, host, queue_name,client_manager):
        threading.Thread.__init__(self)
        self.host = host
        self.client_manager = client_manager
        self.queue_name = queue_name

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.process_message, auto_ack=True)
        print('Listening for messages...')
        channel.start_consuming()

    def process_message(self, channel, method, properties, body):
        result = body.decode()
        result = json.loads(result)
        self.client_manager.send_message_to_client_by_id(result['client_id'], result['message'])
        print("Received message:", result['client_id'])
