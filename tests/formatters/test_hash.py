from logging import makeLogRecord

import pytest

from cryptologging.algorithms.hash import MD5HashEncryptor
from cryptologging.formatter import CryptoFormatter


# @pytest.mark.parametrize(
#     ('value', 'value_hash', 'result'),
#     [
#         pytest.param(
#             'string',
#             'b45cffe084dd3d20d928bee85e7b0f21',
#             'string',
#             id='string_value',
#         ),
#         pytest.param(
#             1,
#             'c4ca4238a0b923820dcc509a6f75849b',
#             '1',
#             id='int_value',
#         ),
#         pytest.param(
#             0.5,
#             'd310cb367d993fb6fb584b198a2fd72c',
#             '0.5',
#             id='float_value',
#         ),
#         pytest.param(
#             b'hello',
#             '5d41402abc4b2a76b9719d911017c592',
#             '"b\'hello\'"',
#             id='byte_value',
#         ),
#         pytest.param(
#             None,
#             '37a6259cc0c1dae299a7866489dff0bd',
#             'null',
#             id='none_value',
#         ),
#         pytest.param(
#             [],
#             'd751713988987e9331980363e24189ce',
#             '[]',
#             id='empty_list',
#         ),
#         pytest.param(
#             ['hello', 1, 3.14, b'hello'],
#             'b79f61f48f9c9a7ec910e896275d334e',
#             '["hello",1,3.14,"b\'hello\'"]',
#             id='list_of_primitive_types_value',
#         ),
#         pytest.param(
#             ('hello', 1, 3.14, b'hello'),
#             'b79f61f48f9c9a7ec910e896275d334e',
#             '["hello",1,3.14,"b\'hello\'"]',
#             id='tuple_of_primitive_types_value',
#         ),
#         pytest.param(
#             (),
#             'd751713988987e9331980363e24189ce',
#             '[]',
#             id='empty_tuple',
#         ),
#         pytest.param(
#             {},
#             '99914b932bd37a50b983c5e7c90ae93b',
#             '{}',
#             id='empty_dict',
#         ),
#         pytest.param(
#             {'key': 'value'},
#             'a7353f7cddce808de0032747a0b7be50',
#             '{"key":"value"}',
#             id='dict_value',
#         ),
#     ]
# )
# def test_formatter(value, value_hash, result):
#     formatter = CryptoFormatter(encryptor=MD5HashEncryptor())
#     assert formatter.format(makeLogRecord({'msg': value})) == result
#
#     formatter = CryptoFormatter(encryptor=MD5HashEncryptor(), encrypt_full_record=True)
#     assert formatter.format(makeLogRecord({'msg': value})) == value_hash


@pytest.mark.parametrize(
    ('value', 'secret_keys', 'result'),
    [
        pytest.param(
            {'key': 'value'},
            {'secret_key', },
            '{"key":"value"}',
            id='has_not_secret_key',
        ),
        pytest.param(
            {'secret_key': 'value'},
            {'secret_key', },
            '{"secret_key":"2063c1608d6e0baf80249c42e2be5804"}',
            id='has_secret_key',
        ),
        pytest.param(
            {'secret_key': 'value', 'secret_key1': 'value'},
            {'secret_key', 'secret_key1'},
            '{"secret_key":"2063c1608d6e0baf80249c42e2be5804","secret_key1":"2063c1608d6e0baf80249c42e2be5804"}',
            id='has_2_secret_keys',
        ),
        pytest.param(
            {'key': {'secret_key': 'value'}},
            {'secret_key', },
            '{"key":{"secret_key":"2063c1608d6e0baf80249c42e2be5804"}}',
            id='secret_key_in_nested_dict',
        ),
        pytest.param(
            [{'key': {'secret_key': 'value'}}, {'key': 'value'}],
            {'secret_key', },
            '[{"key":{"secret_key":"2063c1608d6e0baf80249c42e2be5804"}},{"key":"value"}]',
            id='list_of_dicts__one_of_them_has_secret_key',
        ),
        pytest.param(
            [{'key': [{'secret_key': 'value', 'key': 'value'}]}, {'key': 'value'}],
            {'secret_key', },
            '[{"key":[{"secret_key":"2063c1608d6e0baf80249c42e2be5804","key":"value"}]},{"key":"value"}]',
            id='list_of_dicts__one_of_them_has_list_of_dicts_with_secret_key',
        ),
    ]
)
def test_encryption_on_secret_fields(value, secret_keys, result):
    formatter = CryptoFormatter(encryptor=MD5HashEncryptor(), secret_keys=secret_keys)
    assert formatter.format(makeLogRecord({'msg': value})) == result
