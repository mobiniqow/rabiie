import socketserver

from socket_server.client import Client


class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = Client(self.request, self.client_address)

        client.handle()
