from .enapicommandwithsvn import ENAPICommandWithSvn
from .exceptions import ENAPILenException

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPIAck(ENAPICommandWithSvn):
    MIN_FARME_LEN = 4
    MAX_FARME_LEN = 4

    def __init__(self, data):
        super().__init__(data)
        if not self.is_frame_complete:
            log.debug("incomplete frame: %s", vars(self))
            raise ENAPILenException("data frame is not complete")
