import logging

import pika


class RabbitMq:
    """
        in class rabbit mq hastesh ke consumer hasho be sorate interface tarif kardam
        va behesh ezafe mikonam
    """

    def __init__(self, url, port, user_name, password, virtual_host, ):
        self.url = url
        self.port = port
        self.user_name = user_name
        self.password = password
        self.virtual_host = virtual_host
        #  list of consumer get and set
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                url, port, virtual_host, pika.PlainCredentials(user_name, password)
            )
        )

        self.channel = self.connection.channel()

    def get_channel(self):
        """
            channel chizi hastesh ke consumer ha rosh savar mishavand
        :return:
        """
        return self.channel

    def start(self):
        """
        starting to consuming
        :return:
        """
        print("[*] Start listening")
        self.channel.start_consuming()
