import pika
import json


def serialize_object(obj):
    return json.dumps(obj)


def send_broker_message(client_id, message, ):
    """
        send message to client by id
        :param client_id:
        :param message:
        :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='message_broker')
    my_object = {
        'client_id': client_id,
        'message': str(message),
    }
    message = serialize_object(my_object)
    channel.basic_publish(exchange='', routing_key='message_broker', body=message)
    connection.close()
