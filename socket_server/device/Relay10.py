from socket_server.utils.ferdosi import Ferdosi


class Relay10Handler:
    def __init__(self, device, client):
        self.device = device
        self.client = client

    def read_state_from_r10(self, message):
        state = message.replace('status_r10=', '')
        ferdosi = Ferdosi()
        js = ferdosi.convert_text_to_json(state)
        self.device.r1 = bool(js['r1'])
        self.device.r2 = bool(js['r2'])
        self.device.r3 = bool(js['r3'])
        self.device.r4 = bool(js['r4'])
        self.device.r5 = bool(js['r5'])
        self.device.r6 = bool(js['r6'])
        self.device.r7 = bool(js['r7'])
        self.device.r8 = bool(js['r8'])
        self.device.r9 = bool(js['r9'])
        self.device.r10 = bool(js['r10'])
        self.device.save()

    def handle_message(self, message):
        if message.startswith("status_r10="):
            self.read_state_from_r10(message)
        elif message.startswith("status_r10?"):
            # Handle sending last state
            self.client.send_message(self.device.get_status())
