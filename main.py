import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.dev'
import django

django.setup()
import random
from socket_server.tcp_server import Server
from socket_server.client_manager import ClientManager


def generate_random_number():
    return random.randint(11111, 35000)


if __name__ == "__main__":
    try:
        HOST = "localhost"
        PORT = generate_random_number()
        client_manager = ClientManager()
        server = Server((HOST, PORT), client_manager)
        server_thread = server.start()
        print(f"Server listening on {HOST}:{PORT}")
        # while True:
        #     pass
    except KeyboardInterrupt:
        server_thread.join()
        server.shutdown()
