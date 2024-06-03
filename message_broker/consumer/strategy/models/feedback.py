from message_broker.consumer.strategy.models.strategy_abs import MessageStrategy
from message_broker.message import Message


class ServerTimeStrategy(MessageStrategy):
    def input(self, message: Message):
        pass

    def output(self, message: Message):
        pass
