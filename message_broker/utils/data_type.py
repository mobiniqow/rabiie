def hex_string_to_decimal(value):
    """
    get string and cast to hex string
    :param value: insert your string value
    :return :hex value
    """
    hex_int = int(value, 16)

    return int(hex(hex_int), 0)


def hex_to_binary(number, domain):
    """
    convert int to binary with domain size
    :param number: this can be int or hex
    :param domain: this binary size and fill with 0  example 111 + domain size 8 => 00000111
    :return: binary number
    """
    number = hex_string_to_decimal(number)
    return bin(number)[2:].zfill(domain)


def binary_to_decimal(binary):
    """
    get binary number and return decimal
    :param binary:binary string type
    :return: decimal int type
    """
    return int(binary, 2)


def binary_to_hex(binary):
    """
    get binary number and return hex
    :param binary:binary string type
    :return: decimal hex type
    """
    return hex(binary_to_decimal(binary))


def hex_to_byte_array(_hex: str):
    """
    get hex number and return bytearray
    :param _hex:hex string type
    :return: bytearray
    """
    _hex = _hex[2:] if _hex.startswith("0x") else _hex
    _hex = _hex if len(_hex) % 2 == 0 else "0" + _hex
    return bytearray.fromhex(_hex)


def string_to_hex(text):
    """
    convert text to hex string
    :param text:
    :return: hex string
    """
    return text.encode().hex()


def hex_to_string(_hex):
    """
    convert hex to text string
    :param _hex:
    :return: string
    """
    return bytes.fromhex(_hex).decode("utf-8")
