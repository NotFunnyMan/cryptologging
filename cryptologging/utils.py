from typing import Any

import orjson


def orjson_dumps(value: Any) -> str:
    """Переопределение orjson на возврат строки.

    Args:
        value: значение, необходимое для строкового представления.

    Returns:
        Переданное значение в строковом представлении.
    """
    return orjson.dumps(value, default=str).decode('utf-8')
