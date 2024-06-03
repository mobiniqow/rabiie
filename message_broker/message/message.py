import json
from datetime import datetime

from django.utils.timezone import get_current_timezone


class Message:
    """
        zaman 28 caracter hex tol darad ke az data bayad joda nemod
        example 30303a30303a30303a30303a3030 ==>
        b''.fromhex("30303a30303a30303a30303a30303a3030").decode("utf-8") ==> 00:00:00:00:00:00
    """
    TOLE_ZAMAN = 34

    def __init__(self, payload, _type, device_id, _datetime=None):
        self.payload = payload
        self.type = _type
        self.device_id = device_id
        self.datetime = _datetime

    @classmethod
    def from_byte(cls, byte):
        body = json.loads(str(byte))
        return cls(payload=body['payload'],device_id=body['device_id'],_type=body['type'])

    def get_time(self):
        if self.datetime is not None:
            return self.datetime
        if len(self.payload) >= 28:
            _datetime = self.payload[self.TOLE_ZAMAN:]
            date_string = b"".fromhex(_datetime).decode("utf-8")
            year, month, day, hour, _min, second = date_string.split(":")
            year, month, day, hour, _min, second = (
                int(year),
                int(month),
                int(day),
                int(hour),
                int(_min),
                int(second),
            )
            # timezone = pytz.timezone("US/Pacific")
            tz = get_current_timezone()
            # dt = datetime(, tzinfo=timezone)
            dt = datetime(year, month, day, hour, min, second, tzinfo=tz)
            return dt.strftime("%y:%m:%d:%H:%M:%S")
        return None

    def get_body(self):
        """
            inja payload ro bar migardonam chon gahi oghat payload akharesh time dare man check mikonam ke
            payload akharesh time hast ya na
            age time dare time ro azash kam mikonam va baghie ro bar migardonam
            :return:
        """
        payload = self.payload if len(self.payload) < self.TOLE_ZAMAN else self.payload[: self.TOLE_ZAMAN]
        return payload
