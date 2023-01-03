# Log encryption

cryptologging - это библиотека для шифрования отдельных данных лога.


## Пример использования
```python
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
```

```python
logger.info('String')
>>> {"timestamp": "2023-01-03T18:04:48.401535", "application": "my_super_application", "message": {"content": {"text": "String"}}, "system": "backend"}
```

```python
logger.info(1)
>>> {"timestamp": "2023-01-03T18:04:48.401584", "application": "my_super_application", "message": {"content": {"text": 1}}, "system": "backend"}
```

```python
logger.info(1.6)
>>> {"timestamp": "2023-01-03T18:04:48.401614", "application": "my_super_application", "message": {"content": {"text": 1.6}}, "system": "backend"}
```

```python
logger.info(b'hello')
>>> {"timestamp": "2023-01-03T18:04:48.401641", "application": "my_super_application", "message": {"content": {"text": "b'hello'"}}, "system": "backend"}
```

```python
logger.info(None)
>>> {"timestamp": "2023-01-03T18:04:48.401664", "application": "my_super_application", "message": {"content": {"text": null}}, "system": "backend"}
```

```python
logger.info([1, 1.5, 'hello', b'hello'])
>>> {"timestamp": "2023-01-03T18:04:48.401685", "application": "my_super_application", "message": {"content": {"text": [1, 1.5, "hello", "b'hello'"]}}, "system": "backend"}
```

```python
logger.info((1, 1.5, 'hello', b'hello'))
>>> {"timestamp": "2023-01-03T18:04:48.401709", "application": "my_super_application", "message": {"content": {"text": [1, 1.5, "hello", "b'hello'"]}}, "system": "backend"}
```

```python
logger.info({1, 1.5, 'hello', b'hello'})
>>> {"timestamp": "2023-01-03T18:04:48.401731", "application": "my_super_application", "message": {"content": {"text": "{1, 'hello', 1.5, b'hello'}"}}, "system": "backend"}
```

```python
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

>>> {
    "timestamp":"2023-01-03T18:04:48.401761",
    "application":"my_super_application",
    "message":{
        "content":{
            "data":{
                "field":"value",
                "int_field":1,
                "float_field":3.14,
                "none_field":null,
                "secret_field":"881671aa2bbc680bc530c4353125052b",
                "nested_field":{
                    "secret_field":"881671aa2bbc680bc530c4353125052b"
                },
                "list_field":[
                    "element1",
                    "element2"
                ],
                "tuple_field":[
                    "t_elem1",
                    "t_elem2"
                ],
                "list_of_secret_data":[
                    {
                        "secret_field":"881671aa2bbc680bc530c4353125052b",
                        "not_secret_field":"value"
                    },
                    {
                        "secret_field":"881671aa2bbc680bc530c4353125052b",
                        "not_secret_field":"value"
                    },
                    [
                        {
                            "secret_field1":"1711df9f5b96b2802fbddf18dec7c570"
                        }
                    ],
                    {
                        "secret_field":"c4ca4238a0b923820dcc509a6f75849b"
                    },
                    {
                        "secret_field":"4beed3b9c4a886067de0e3a094246f78"
                    },
                    {
                        "secret_field":"f79408e5ca998cd53faf44af31e6eb45"
                    },
                    {
                        "not_secret":{
                            "not_secret":{
                                "not_secret":{
                                    "not_secret":{
                                        "not_secret":{
                                            "secret_field2":"37a6259cc0c1dae299a7866489dff0bd"
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
    },
    "system":"backend"
}
```