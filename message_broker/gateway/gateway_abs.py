from abc import ABC, abstractmethod

from message_broker.consumer.strategy.models.strategy_abs import MessageStrategy
from message_broker.message.message import Message


class GatewayAbs:
    __metaclass__ = ABC

    @abstractmethod
    def input(self, message: Message) -> None:
        pass

    @abstractmethod
    def output(self, message: Message) -> None:
        pass

    @abstractmethod
    def add_strategy(self, strategy: MessageStrategy) -> None:
        pass
