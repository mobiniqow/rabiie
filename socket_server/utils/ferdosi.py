from rest_framework.utils import json


class Ferdosi:
    def convert_text_to_json(self, text):
        key_value_pairs = [value.split('=') for value in text.split(',')]
        data = {key: int(value) for key, value in key_value_pairs}
        json_data = json.dumps(data)
        return json.loads(json_data)
