
import json

from device.models import Relay6, Relay10
from socket_server.client_manager import ClientManager


class Client:
    def __init__(self, client, client_id):
        self.client = client
        self.client_id = client_id

    def send_message(self, message):
        print(message)
        self.client.send(message.encode())

    def disconnect(self):
        self.client.close()

    def update(self, data):
        pass
        # url = "localhost:8000/api/device/socket/" + self.client_id + "/"
        # method = "PATCH"
        # payload = data.encode()
        #
        # headers = {
        #     "Content-Type": "application/x-www-form-urlencoded",
        # }
        #
        # conn = http.client.HTTPConnection("localhost", 8000)
        # conn.request(method, url, body=payload, headers=headers)
        #
        # res = conn.getresponse()
        # data = res.read()
        #
        # print(data.decode())
        #
        # conn.close()

    def handle(self):
        print(f"Client connected: {self.client_id}")
        while True:
            try:
                message = self.client.recv(1024).decode()
                if not message:
                    break
                print(f"Received message from client {self.client_id}: {message}")
                print(message)

                # 🤑
                if message.startswith("ID"):
                    product_id = message.split("=")[1]
                    var = Relay10.objects.filter(product_id=product_id)
                    print(var)




            except ConnectionResetError:
                break
