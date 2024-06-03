from abc import ABC, abstractmethod

from message_broker.gateway.gateway_abs import GatewayAbs


class ConsumerObserver:
    __metaclass__ = ABC

    def __init__(self, gateway_abs: GatewayAbs):
        self.gateway = gateway_abs

    @abstractmethod
    def __call__(self, ch, method, properties, body):
        """
            in method in ye magic method hastesh va be ma in emkan ro mide
            ke be onvane yek function yek object ro betonim call konim
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        pass
