import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def isValidPhone(input: str):
    if not re.match(r'^09\d{9}$', input):
        raise ValidationError(f'{input} invalid phone number')


def isValidPassword(input: str):
    try:
        validate_password(input)
    except:
        return False
    return True


def is_number(value):
    """
    :param value: get string for validate
    :return: exception if not valid number
    """
    if not value.isnumeric():
        raise Exception('is not number')


def isValidEmail(input: str):
    if not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", input):
        raise ValidationError(f'{input} invalid Email')


def isValidName(input: str):
    if not re.match(r"[\W_]+", input):
        raise ValidationError(
            f"{input} invalid Username, Don't use (Any non-word character and '_' )!")


def isValidPasswordStrong(input: str):
    score = 0
    if len(input) < 8:
        raise ValidationError(f"Password must not be less than 8 character.")
    if re.findall(r'[_\-\[\]{};.: ]+', input):
        raise ValidationError(
            "Don't use( _-[]{};.:, and White-space) in Password !")
    if len(input) > 20:
        score += 1
    if re.findall(r'[a-z]+', input):
        score += 1
    if re.findall(r'[A-Z]+', input):
        score += 1
    if re.findall(r'\d+', input):
        score += 1
    if re.findall(r'\W+', input):
        score += 1
    return score


def isValidPhone(input: str):
    return len(input)>8
    # if not re.match(r'^09\d{9}$', input):
    #    raise ValidationError(f'{input} invalid phone number')


def isValidPhoneNumber(inp):
    return len(inp)>8
    # return True
    # return re.match(r'^09\d{9}$', inp)


def isValidPassword(input: str):
    try:
        validate_password(input)
    except Exception as e:
        return False
    return True


def isValidEmail(input: str):
    if not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", input):
        raise ValidationError(f'{input} invalid Email')


def isValidName(input: str):
    if not re.match(r"[\W_]+", input):
        raise ValidationError(
            f"{input} invalid Username, Don't use (Any non-word character and '_' )!")


def isValidPasswordStrong(input: str):
    score = 0
    if len(input) < 8:
        raise ValidationError(f"Password must not be less than 8 character.")
    if re.findall(r'[_\-\[\]{};.: ]+', input):
        raise ValidationError(
            "Don't use( _-[]{};.:, and White-space) in Password !")
    if len(input) > 20:
        score += 1
    if re.findall(r'[a-z]+', input):
        score += 1
    if re.findall(r'[A-Z]+', input):
        score += 1
    if re.findall(r'\d+', input):
        score += 1
    if re.findall(r'\W+', input):
        score += 1
    return score


def getPhone(phone):
    if (phone.startswith("098") | phone.startswith("+98")):
        return f'{0}{phone[3:]}'
    elif phone.startswith("9"):
        return f'{0}{phone}'
    else:
        return phone


def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input):
        return False

    check = int(input[9])
    s = sum(map(lambda x: int(input[x]) * (10 - x), range(0, 9))) % 11
    return (s < 2 and check == s) or (s >= 2 and check + s == 11)


def mosabat(val):
    return float(val) >= 0
