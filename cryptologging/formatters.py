from logging import Formatter, LogRecord


class CryptoFormatter(Formatter):
    """Formatter with encryption."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record: LogRecord):
        super().format(record)
