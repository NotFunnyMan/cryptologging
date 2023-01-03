from abc import abstractmethod
from logging import Formatter, LogRecord
from typing import Any, Callable, Literal, Optional

from cryptologging.algorithms.abstract import AbstractEncryptor
from cryptologging.utils import orjson_dumps


class CryptoFormatter(Formatter):
    """Форматтер записи лога."""

    def __init__(
        self,
        encryptor: AbstractEncryptor,
        secret_keys: Optional[set[str]] = None,
        json_dumps: Callable = orjson_dumps,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal['%', '{', '$'] = '%',
        validate: bool = True,
        encrypt_full_record: bool = False,
    ):
        """Инициализация шифрующего Formatter-а.

        Args:
            encryptor: шифровальщик данных.
            secret_keys: ключи словаря, которые будут зашифрованы.
            json_dumps: переводчик лога в строковое представление.
            fmt: формат записи лога.
            datefmt: формат даты.
            style: стиль форматирования.
            validate: валидация формата стиля.
            encrypt_full_record: шифровать ли всю лог-строку целиком.
        """
        self.encryptor = encryptor
        self._secret_keys = set(secret_keys) if secret_keys else ()
        self._encrypt_full_record = encrypt_full_record
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
        )
        self._dumps = json_dumps
        self._array_types = (list, tuple, set)

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Отформатировать указанную запись как текст.

        Args:
            record: запись лога.

        Returns:
            Запись лога в строковом представлении.
        """
        encrypted_record = self.encrypt(record.msg)
        if isinstance(encrypted_record, str):
            return encrypted_record
        return self._dumps(encrypted_record)

    def encrypt(self, message: Any) -> Any:
        """Зашифровать запись.

        Args:
            message: сообщение лога.

        Returns:
            зашифрованное сообщение лога.
        """

        if self._encrypt_full_record:
            return self.encryptor.encrypt(None, message)

        if isinstance(message, (*self._array_types, dict)):
            return self._bypass_in_depth(None, message)
        return message

    def _bypass_in_depth(self, key: Optional[Any], value: Any) -> Any:
        """Обход записи лога в глубину."""
        if key in self._secret_keys:
            return self.encryptor.encrypt(key, value)
        elif isinstance(value, dict):
            return {
                k: self._bypass_in_depth(k, value[k]) for k, v in value.items()
            }
        elif isinstance(value, self._array_types):
            type_ = type(value)
            return type_(self._bypass_in_depth(key, v) for v in value)
        return value
