import random
from typing import List

RANDOM_LENGTH = 3
BASE_62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


# This function is just for testing.
def _base62_string_to_decimal(base62_string: str) -> int:
    number_list = list(map(BASE_62_DIGITS.index, base62_string))
    result = 0
    for num, i in zip(number_list, reversed(range(len(number_list)))):
        result += num * 62 ** i
    return result


def _decimal_to_base62(number: int) -> List[int]:
    result = []
    while number > 0:
        remainder = number % 62
        result.append(remainder)
        number = int(number / 62)
    return list(reversed(result))


def _base62_to_string(number_list: List[int]) -> str:
    result = map(lambda n: BASE_62_DIGITS[n], number_list)
    return "".join(result)


def _generate_random_string(length: int) -> str:
    result = random.sample(BASE_62_DIGITS, length)
    return "".join(result)


def generate_url_id(counter: int) -> str:
    """Based on the integer value of the counter, generate an URL ID in the alphanumeric format."""
    base62_list = _decimal_to_base62(counter)
    base62_string = _base62_to_string(base62_list)
    random_part = _generate_random_string(RANDOM_LENGTH)
    return random_part + base62_string
