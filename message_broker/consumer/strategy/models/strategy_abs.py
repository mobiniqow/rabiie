from abc import ABC, abstractmethod

from message_broker.message import Message


class MessageStrategy(ABC):
    # in code unique hastesh yeki bare get hastesh yeki baraye set
    # get ha az samte client be ma mian
    # set ha az samte ma be client miravand



    def __init__(self, message: Message, set_cod: str, get_cod: str):
        self.message: Message = message
        self.set_cod = set_cod
        self.get_cod = get_cod


    @abstractmethod
    def do_get(self):
        """
            :var self.get_code
            message broker tanzimate akhar ro gerefte va be client pass midahad
        """
        pass

    @abstractmethod
    def do_set(self):
        """
            :var self.se_code
            message broker tanzimate akhar az client gerefte va time ro dar nazar gerefte va set mikonad
        """
        pass
