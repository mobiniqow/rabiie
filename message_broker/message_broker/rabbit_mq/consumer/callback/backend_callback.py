import json
import ast
import json
from message_broker.consumer.strategy.models.settings import SettingsStrategy
from message_broker.gateway.gateway import GateWay
from message_broker.message.message import Message
from message_broker.message_broker.rabbit_mq.consumer.callback.consumer_observer_abs import ConsumerObserver
from message_broker.utils.data_type import string_to_hex


class BackendCallBack(ConsumerObserver):

    def __call__(self, ch, method, properties, body):
        print(f'body {ast.literal_eval(json.dumps(body.decode("utf-8")))}')
        message=Message.from_byte(ast.literal_eval(json.dumps(body.decode("utf-8"))))
        self.gateway.input(message)

