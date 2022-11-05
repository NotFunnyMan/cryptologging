from hashlib import md5, sha256, sha512
from typing import Any, Callable

from cryptologging.algorithms.abstract import AbstractEncryptor, orjson_dumps


class BaseHashEncryptor(AbstractEncryptor):
    """Шифрует значения с помощью заданного алгоритма хэширования."""

    def __init__(
        self,
        algorithm = md5,
        json_dumps: Callable = orjson_dumps,
    ):
        super().__init__(json_dumps)
        self._algorithm = algorithm

    def encrypt(self, key: Any, value: Any) -> str:
        """Зашифровать значение."""
        if isinstance(value, (bytes, bytearray)):
            return self._algorithm(value).hexdigest()
        if isinstance(value, str):
            return self._algorithm(value.encode()).hexdigest()
        return self._algorithm(self._dumps(value).encode()).hexdigest()


class MD5HashEncryptor(BaseHashEncryptor):
    """Шифрование данных с помощью md5."""

    def __init__(self, algorithm=md5, json_dumps=orjson_dumps):
        """Инициализация шифровальщика, использующего алгоритм md5."""
        super().__init__(algorithm, json_dumps)


class Sha256HashEncryptor(BaseHashEncryptor):
    """Шифрование данных с помощью sha256."""

    def __init__(self, algorithm=sha256, json_dumps=orjson_dumps):
        """Инициализация шифровальщика, использующего алгоритм sha256."""
        super().__init__(algorithm, json_dumps)


class Sha512HashEncryptor(BaseHashEncryptor):
    """Шифрование данных с помощью sha512."""

    def __init__(self, algorithm=sha512, json_dumps=orjson_dumps):
        """Инициализация шифровальщика, использующего алгоритм sha512."""
        super().__init__(algorithm, json_dumps)
