import socketserver
import threading
from socket_server.client_handler import ClientHandler


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, client_manager):
        super().__init__(server_address, ClientHandler)
        self.client_manager = client_manager

    def start(self):
        server_thread = threading.Thread(target=self.serve_forever)
        server_thread.start()
