from datetime import datetime

from django.utils.timezone import get_current_timezone


class Message:
    """
        zaman 28 caracter hex tol darad ke az data bayad joda nemod
        example 30303a30303a30303a30303a3030 ==>
        b''.fromhex("30303a30303a30303a30303a30303a3030").decode("utf-8") ==> 00:00:00:00:00:00
    """
    TOLE_ZAMAN = 19

    def __init__(self, payload, _type, device_id, _datetime=None):
        self.payload = payload
        self.type = _type
        self.device_id = device_id
        self.datetime = _datetime

    @classmethod
    def from_byte(cls, body):
        print(f'body2 {body}')
        # body = byte
        # payload = body['payload'] if len(body['payload']) > 0 else ""
        # _datetime = body['datetime'] if len(body['datetime']) > 0 else ""
        # _type = body['type'] if len(body['type']) > 0 else ""
        # device_id = body['device_id'] if len(body['device_id']) > 0 else ""
        return cls(body['payload'],  body['type'],body['device_id'],  body['datetime'])

    def get_time(self):
        if self.datetime is None or self.datetime == "":
            return ""
        else:
            print(f'self.datetime {self.datetime}')
            year, month, day, hour, _min, second = self.datetime.split(":")
            year, month, day, hour, _min, second = (
                int(year),
                int(month),
                int(day),
                int(hour),
                int(_min),
                int(second),
            )
            tz = get_current_timezone()
            dt = datetime(year, month, day, hour, _min, second, tzinfo=tz)
            return dt


    def get_body(self):
        """
            inja payload ro bar migardonam chon gahi oghat payload akharesh time dare man check mikonam ke
            payload akharesh time hast ya na
            age time dare time ro azash kam mikonam va baghie ro bar migardonam
            :return:
        """
        payload = self.payload if len(self.payload) < self.TOLE_ZAMAN else self.payload[: -self.TOLE_ZAMAN]
        return payload
