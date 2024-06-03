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

    def add_client(self, client, client_id):
        with self.mutex:
            client.send(b"ID?")
            key_val = f"{client_id[0]}:{client_id[1]}"  # client_id[0] is the ip and client_id[1] is the port
            self.clients_product_id[key_val] = client
            print(f"client add {client_id}")
            self.clients[key_val] = client

    def remove_client(self, client):
        with self.mutex:
            del self.clients[client.client_id]

    def find_client_by_id(self, client_id):
        with self.mutex:
            return self.clients.get(client_id)

    def send_message_to_client_by_id(self, client_id, message):
        with self.mutex:
            client = self.clients.get(client_id)
            if client:
                client.send(message.encode())

    def get_status(self, client_id):
        with self.mutex:
            client = self.clients.get(client_id)
            if client:
                client.send_message("Status?")
