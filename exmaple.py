import logging
from cryptologging.hashing.formatter import HashFormatter

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(HashFormatter('%(name)-12s: %(levelname)-8s %(message)s'))
logger.addHandler(handler)

logger.info('Test')
