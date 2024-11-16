from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel

from message_broker.message_broker.rabbit_mq.consumer.callback.consumer_observer_abs import (
    ConsumerObserver,
)


class RabbitMQConsumerABS(object):
    __metaclass__ = ABC
    """
    in yek abstraction az model koli az rabbitmq consumer hastesh
    consumer yani masraf konande yani kasi ke data ro masraf mikone va estefade mikone
    """

    def __init__(
        self,
        channel: BlockingChannel,
        observable: ConsumerObserver,
        routing_key,
        exchange,
        queue,
    ):
        channel.queue_declare(queue=queue)
        channel.exchange_declare(exchange=exchange, exchange_type="direct")
        channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
        )
        # dar inja man class observer ro beheshe pass dadam be onvan yek method
        channel.basic_consume(
            queue=queue, on_message_callback=observable, auto_ack=True
        )

    # def __call__(self, ch, method, properties, body):
    #     """
    #         in method in ye magic method hastesh va be ma in emkan ro mide
    #         ke be onvane yek function yek object ro betonim call konim
    #     :param ch:
    #     :param method:
    #     :param properties:
    #     :param body:
    #     :return:
    #     """
    #     pass
