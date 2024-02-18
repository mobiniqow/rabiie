from socket_server.utils.ferdosi import Ferdosi


class Relay10Handler:
    def __init__(self, device, client):
        self.device = device
        self.client = client

    def read_state_from_r10(self, message):
        state = message.replace('status_r10=', '')
        ferdosi = Ferdosi()
        js = ferdosi.convert_text_to_json(state)
        print(js)
        if 'r1' in js:
            print('r1', js['r1'])
            self.device.r1 = bool(js['r1'])
        if 'r2' in js:
            print('r2', js['r2'])
            self.device.r2 = bool(js['r2'])
        if 'r3' in js:
            self.device.r3 = bool(js['r3'])
        if 'r4' in js:
            self.device.r4 = bool(js['r4'])
        if 'r5' in js:
            self.device.r5 = bool(js['r5'])
        if 'r6' in js:
            self.device.r6 = bool(js['r6'])
        if 'r7' in js:
            self.device.r7 = bool(js['r7'])
        if 'r8' in js:
            self.device.r8 = bool(js['r8'])
        if 'r9' in js:
            self.device.r9 = bool(js['r9'])
        if 'r10' in js:
            self.device.r10 = bool(js['r10'])
        self.device.save()

    def handle_message(self, message):
        if message.startswith("status_r10="):
            self.read_state_from_r10(message)
        elif message.startswith("status_r10?"):
            # Handle sending last state
            self.client.send_message(self.device.get_status())
