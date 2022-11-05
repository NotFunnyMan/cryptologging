from abc import ABC, abstractmethod
from typing import Any, Callable

from cryptologging.utils import orjson_dumps


class AbstractEncryptor(ABC):
    """Абстрактный класс, реализующий API шифровальщика данных."""

    def __init__(
        self,
        json_dumps: Callable = orjson_dumps,
    ):
        """Инициализация шифровальщика.

        Args:
            json_dumps: метод, переводящий данные в строку.
        """
        self._dumps = json_dumps

    @abstractmethod
    def encrypt(self, key: Any, value: Any) -> str:
        """Зашифровать значение.

        Args:
            key: ключ, если значение было взято из словаря.
            value: значение, подлежащее шифрованию.

        Returns:
            Зашифрованное значение.
        """
