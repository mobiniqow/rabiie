import ast
import json

from message_broker.message.message import Message
from message_broker.message_broker.rabbit_mq.consumer.callback.consumer_observer_abs import ConsumerObserver


class BackendCallBack(ConsumerObserver):

    def __call__(self, ch, method, properties, body):
        print(f'body {ast.literal_eval(json.dumps(body.decode("utf-8")))}')
        message = Message.from_byte(json.loads(ast.literal_eval(json.dumps(body.decode("utf-8")))))

        print(message)
        self.gateway.input(message)
