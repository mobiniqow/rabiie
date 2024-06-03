from abc import ABC, abstractmethod

from message_broker.message.message import Message


class MessageStrategy(ABC):
    # in code unique hastesh yeki bare get hastesh yeki baraye set
    # get ha az samte client be ma mian
    # set ha az samte ma be client miravand

    @abstractmethod
    def input(self, message: Message):
        """
        :var self.get_code
        message broker tanzimate akhar ro gerefte va be client pass midahad
        """
        pass

    @abstractmethod
    def output(self, message: Message):
        """
        :var self.se_code
        message broker tanzimate akhar az client gerefte va time ro dar nazar gerefte va set mikonad
        """
        pass

    @abstractmethod
    def get_code(self) -> str:
        """
        return 2 character cod
        :return:
        """
        pass
