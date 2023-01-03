import json
import logging
from datetime import datetime

from cryptologging.algorithms.hash import MD5HashEncryptor
from cryptologging.formatter import CryptoFormatter

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()


class MySuperFormatter(CryptoFormatter):
    """Форматтер, используемый в моей команде."""

    def format(self, record: logging.LogRecord):
        """Форматирование записи лога."""
        formatted_record = {
            'timestamp': datetime.now().isoformat(),
            'application': 'my_super_application',
            'message': {
                'content': {
                    'data': self.encrypt(record.msg),
                } if isinstance(record.msg, dict) else {
                    'text': record.msg,
                },
            },
            'system': 'backend',
        }
        return json.dumps(formatted_record, default=str)


handler.setFormatter(
    MySuperFormatter(
        encryptor=MD5HashEncryptor(),
        secret_keys={
            'secret_field', 'secret_field1', 'secret_field2',
        },
    ),
)
logger.addHandler(handler)

logger.info('String')
logger.info(1)
logger.info(1.6)
logger.info(b'hello')
logger.info(None)
logger.info([1, 1.5, 'hello', b'hello'])
logger.info((1, 1.5, 'hello', b'hello'))
logger.info({1, 1.5, 'hello', b'hello'})
logger.info(
    {
        'field': 'value',
        'int_field': 1,
        'float_field': 3.14,
        'none_field': None,
        'secret_field': 'secret_value',
        'nested_field': {
            'secret_field': 'secret_value',
        },
        'list_field': [
            'element1', 'element2',
        ],
        'tuple_field': (
            't_elem1', 't_elem2',
        ),
        'list_of_secret_data': [
            {
                'secret_field': 'secret_value',
                'not_secret_field': 'value',
            },
            {
                'secret_field': 'secret_value',
                'not_secret_field': 'value',
            },
            [
                {
                    'secret_field1': ['secret_value'],
                },
            ],
            {
                'secret_field': 1,
            },
            {
                'secret_field': 3.14,
            },
            {
                'secret_field': (1, 2),
            },
            {
                'not_secret': {
                    'not_secret': {
                        'not_secret': {
                            'not_secret': {
                                'not_secret': {
                                    'secret_field2': None,
                                },
                            },
                        },
                    },
                },
            },
        ],
    },
)
