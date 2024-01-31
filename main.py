import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.dev'
import django

django.setup()
from socket_server.tcp_server import Server
from socket_server.client_manager import ClientManager

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 1213
    client_manager = ClientManager()
    server = Server((HOST, PORT), client_manager)
    server.start()
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown()
