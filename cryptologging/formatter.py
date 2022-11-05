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
        fields: Optional[set[str]] = None,
        json_dumps: Callable = orjson_dumps,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal['%', '{', '$'] = '%',
        validate: bool = True,
    ):
        """Инициализация шифрующего Formatter-а.

        Args:
            encryptor: шифровальщик данных.
            fields: поля у словаря, которые будут зашифрованы.
            json_dumps: переводчик лога в строковое представление.
            fmt: формат записи лога.
            datefmt: формат даты.
            style: стиль форматирования.
            validate: валидация формата стиля.
        """
        self.encryptor = encryptor
        self._fields = set(fields) if fields else ()
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
        )
        self._dumps = json_dumps
        self._iterable_types = (list, tuple, set)

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Отформатировать указанную запись как текст.

        Args:
            record: запись лога.

        Returns:
            Запись лога в строковом представлении.
        """
        return self._dumps(self.encrypt(record.msg))

    def encrypt(self, record: Any) -> Any:
        """Зашифровать запись.

        Args:
            record: запись лога.

        Returns:
            зашифрованная запись лога.
        """
        message = None
        if isinstance(record, (*self._iterable_types, dict)):
            message = self._bypass_in_depth(None, record)
        else:
            message = self.encryptor.encrypt(None, record)
        return message

    def _bypass_in_depth(self, key: Optional[Any], value: Any) -> Any:
        """Обход записи лога в глубину."""
        if key in self._fields:
            return self.encryptor.encrypt(key, value)
        elif isinstance(value, dict):
            return {
                k: self._bypass_in_depth(k, value[k]) for k, v in value.items()
            }
        elif isinstance(value, self._iterable_types):
            type_ = type(value)
            return type_(self._bypass_in_depth(key, v) for v in value)
        return value
