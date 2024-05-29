import os

from socket_server.message_broker_consumer.message_broker import MessageListenerThread

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.dev'
import django

django.setup()
import random
from socket_server.tcp_server import Server
from socket_server.client_manager import ClientManager


# def generate_random_number():
#     return random.randint(11111, 35000)


def start_listening(client_manager):
    listener_thread = MessageListenerThread('localhost', 'backend_queue',client_manager)
    listener_thread.start()


if __name__ == "__main__":
    try:
        client_manager = ClientManager()
        # server = Server((HOST, PORT), client_manager)
        start_listening(client_manager)
        # server_thread = server.start()
        # while True:
        #     pass
    except KeyboardInterrupt:
        pass
        # server_thread.join()
        # server.shutdown()

# تابع start_listening() را فراخوانی کنید تا ترد راه‌اندازی شود

