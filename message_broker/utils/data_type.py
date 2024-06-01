def hex_string_to_int(value):
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
    number = hex_string_to_int(number)
    return bin(number)[2:].zfill(domain)
