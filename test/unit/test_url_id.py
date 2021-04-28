from unittest.mock import patch as mock_patch

import pytest

from shortener import url_id


@pytest.mark.parametrize(
    "test_input,result", [(125, [2, 1]), (25, [25]), (1000, [16, 8])]
)
def test_decimal_to_base62(test_input, result):
    assert url_id._decimal_to_base62(test_input) == result


@pytest.mark.parametrize(
    "test_input,result", [([2, 1], "21"), ([24], "O"), ([16, 8], "G8")]
)
def test_base62_to_string(test_input, result):
    assert url_id._base62_to_string(test_input) == result


@pytest.mark.parametrize(
    "test_input,result", [("21", 125), ("O", 24), ("G8", 1000), ("e9a", 154354)]
)
def test_base62_string_to_decimal(test_input, result):
    assert url_id._base62_string_to_decimal(test_input) == result


@pytest.mark.parametrize("input_length,output_length", [(3, 3), (5, 5)])
def test_generate_random_string(input_length, output_length):
    _string = url_id._generate_random_string(input_length)
    assert len(_string) == output_length


@pytest.mark.parametrize(
    "counter,result",
    [(1, "abc1"), (10, "abcA"), (125, "abc21"), (1000, "abcG8"), (154354, "abce9a")],
)
def test_generate_url_id(counter, result):
    with mock_patch("test.unit.test_url_id.url_id._generate_random_string") as method:
        method.return_value = "abc"
        assert url_id.generate_url_id(counter) == result
