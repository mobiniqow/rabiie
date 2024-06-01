import pytz


class Message:
    #  zaman 28 caracter hex tol darad ke az data bayad joda nemod
    #  example 30303a30303a30303a30303a3030 ==> b''.fromhex("30303a30303a30303a30303a30303a3030").decode("utf-8") ==> 00:00:00:00:00:00
    TOLE_ZAMAN = 34

    def __init__(self, payload, _type, device_id, ):
        self.payload = payload
        self.type = _type
        self.device_id = device_id

    def get_time(self):
        if len(self.payload) >= 28:
            datetime = self.payload[self.TOLE_ZAMAN:]
            date_string = b''.fromhex(datetime).decode("utf-8")
            year, month, day, hour, min, second = date_string.split(":")
            year, month, day, hour, min, second = int(year), int(month), int(day), int(hour), int(min), int(second)
            timezone = pytz.timezone('US/Pacific')
            # dt = datetime(, tzinfo=timezone)
            dt = datetime(year, month, day, hour, min, second, tzinfo=timezone)
