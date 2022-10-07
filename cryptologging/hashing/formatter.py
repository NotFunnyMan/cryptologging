from logging import Formatter, LogRecord
from hashlib import md5


class HashFormatter(Formatter):
    """Formatter with hashing."""

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style='%',
        validate=True,
        algorithm=md5,
    ):
        self.algorithm = algorithm
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            validate=validate
        )

    def format(self, record: LogRecord) -> str:
        """Format log record depends on algorithm."""
        return self.algorithm(record.getMessage().encode()).hexdigest()
