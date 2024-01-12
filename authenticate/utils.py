import json
import string
from threading import Thread
import requests


def get_or_default(request, _input, default_value):
    try:
        return request.data[_input]
    except Exception as _:
        return default_value


def input_or_default(_input, default_value):
    return _input if _input else default_value


def nextpay_first(amount, order_id, customer_phone):
    WALLET_API_KEY = 'a186c15f-53ef-4490-9059-1a700666ebc8'
    url = "https://nextpay.org/nx/gateway/token"

    payload = f"api_key={WALLET_API_KEY}&amount={amount}&order_id={order_id}&customer_phone={customer_phone}&callback_uri=http://localhost:8000/wallet/"
    headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data


def nextpay_verify(amount, trans_id):
    WALLET_API_KEY = 'a186c15f-53ef-4490-9059-1a700666ebc8'
    url = "https://nextpay.org/nx/gateway/verify"

    payload = f'api_key={WALLET_API_KEY}&amount={amount}&trans_id={trans_id}'
    headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data


def rand_generator(size=6, chars=string.ascii_uppercase + string.digits):
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def getRandomGenerator(size: int):
    import string
    import secrets
    alphabet = string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(size))
    return password


def getRandomGeneratorString(size: int):
    import uuid
    password = uuid.uuid4().hex[:size]
    return password


def getRandomGenerator(size: int):
    import string
    import secrets
    alphabet = string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(size))
    return password


def getRandomGeneratorString(size: int):
    import uuid
    password = uuid.uuid4().hex[:size]
    return password


def sendMessage(phone, code):
    Thread(target=sms, args=(phone, code)).start()


def sms(_phone, _message):
    url = "https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"

    payload = f'username=09113569404&password=Mel1p@y4m@k&text={_message}&to={_phone}&bodyId=168856'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


def share_link(_phone, title, music_url):
    url = "https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
    payload = f'username=09113569404&password=Mel1p@y4m@k&text={title},{music_url}&to={_phone}&bodyId=168856'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
