import logging
from logging import INFO

from message_broker.consumer.strategy.models.strategy_abs import MessageStrategy
from message_broker.gateway.gateway_abs import GatewayAbs
from message_broker.message.message import Message


class GateWay(GatewayAbs):
    """
    in ye class hastesh ke payam haro bar assase type hashon
    be sterategy haie mokhtalef hedayat mikone
    """

    def __init__(self):
        self.__strategies = {}

    def message(self):
        pass

    def add_strategy(self, strategy: MessageStrategy):
        logging.log(INFO, "add strategy successfully with code" )
        self.__strategies[strategy.get_code()] = strategy

    def input(self, message: Message):
        """
        az device message ro migire va motenaseb ba strategy kari ke bayad ro anjam mide
        :param message:
        :return: felen chizi bar nemigardone valie dar ayande shayad ye tedad flag bar gardondam
        """
        if message.type[0]=="W":
            message.type = f'R{message.type[1]}'
        strategy: MessageStrategy = self.__strategies[message.type]
        strategy.input(message)

    def output(self, message: Message):
        """
        az device message ro migire va motenaseb ba strategy kari ke bayad ro anjam mide
        :param message:
        :return:
        """
        strategy: MessageStrategy = self.__strategies[message.type]
        strategy.output(message)
