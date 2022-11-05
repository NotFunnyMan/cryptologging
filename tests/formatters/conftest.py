import logging

import pytest

from cryptologging.formatter import CryptoFormatter
from cryptologging.algorithms.hash import MD5HashEncryptor


@pytest.fixture()
def flogger():
    hash_logger = logging.getLogger('hash_logger')
    hash_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(CryptoFormatter(encryptor=MD5HashEncryptor()))
    hash_logger.addHandler(handler)
    return hash_logger
