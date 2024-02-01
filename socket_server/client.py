import json

from device.models import Relay6, Relay10
from socket_server.client_manager import ClientManager
from socket_server.device.Relay10 import Relay10Handler


class Client:
    def __init__(self, client, client_id):
        self.client = client
        self.client_id = client_id
        self.connected = True
        self.product_id = None
        self.device = None

    def send_message(self, message):
        self.client.send(message.encode())

    def disconnect(self):
        self.connected = False
        self.client.close()

    def update(self, data):
        pass
        # Implement update logic

    def check_id(self, message):
        product_id = message.split("=")[1]
        var = Relay10.objects.filter(product_id=product_id)
        if not var.exists():
            self.connected = False
            self.disconnect()
            print(f"Device not found with {product_id} for client{self.client_id}")
        else:
            self.device = var[0]
            self.device.client_id = self.client_id
            self.product_id = product_id
            self.device.save()
            self.relay10_handler = Relay10Handler(self.device, self)

    def handle(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode()
                if not message:
                    break

                if message.startswith("ID"):
                    self.check_id(message)
                else:
                    if not self.device:
                        self.disconnect()

                self.relay10_handler.handle_message(message)

            except ConnectionResetError:
                break
