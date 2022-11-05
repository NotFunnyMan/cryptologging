import pytest


@pytest.mark.parametrize(
    ('value', 'result'),
    [
        pytest.param(
            'string',
            'b45cffe084dd3d20d928bee85e7b0f21',
            id='string_value',
        ),
        pytest.param(
            1,
            'c4ca4238a0b923820dcc509a6f75849b',
            id='int_value',
        ),
        pytest.param(
            0.5,
            'd310cb367d993fb6fb584b198a2fd72c',
            id='float_value',
        ),
        pytest.param(
            b'hello',
            '5d41402abc4b2a76b9719d911017c592',
            id='byte_value',
        ),
        pytest.param(
            [],
            '5d41402abc4b2a76b9719d911017c592',
            id='empty_list',
        ),
        pytest.param(
            ['hello', 1, 3.14, b'hello'],
            '5d41402abc4b2a76b9719d911017c592',
            id='list_of_primitive_types_value',
        ),
    ]
)
def test_record_as_string(caplog, flogger, value, result):
    """Логируемое сообщение - строка."""
    flogger.info(value)
    for record in caplog.records:
        assert record.msg == result
