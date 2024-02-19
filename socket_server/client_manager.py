import threading


class ClientManager:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.clients = {}
        self.clients_product_id = {}
        self.mutex = threading.RLock()

    def add_client(self, client):
        with self.mutex:

            client.send(b"ID?")
            self.clients[client.id] = client

    def remove_client(self, client):
        with self.mutex:
            del self.clients[client.client_id]

    def find_client_by_id(self, client_id):
        with self.mutex:
            return self.clients.get(client_id)

    def send_message_to_client_by_id(self, client_id, message):
        with self.mutex:
            client = self.clients.get(client_id)
            print(f'client {self.clients}')
            if client:
                client.send_message(message)

    def get_status(self, client_id):
        with self.mutex:
            client = self.clients.get(client_id)
            if client:
                client.send_message("Status?")
