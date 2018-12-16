from .exceptions import ENAPILenException, ENAPICommandTypeNotImplementedException

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPI(object):
    MIN_FARME_LEN = 2
    MAX_FARME_LEN = 999999 # FIXME use maximum possible value

    @property
    def min_frame_len(self):
        return self.__class__.MIN_FARME_LEN

    @property
    def max_frame_len(self):
        return self.__class__.MAX_FARME_LEN

    def __init__(self, data):
        self.data = data
        if len(data) < self.min_frame_len:
            log.debug("too short frame: %d < %d: %s -> %s", len(data), self.min_frame_len, data, vars(self))
            raise ENAPILenException("data frame is too short")
        if len(data) > self.max_frame_len:
            log.debug("too long frame: %d > %d: %s -> %s", len(data), self.max_frame_len, data, vars(self))
            raise ENAPILenException("data frame is too long")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def is_frame_len_possible(self):
        return len(self.data) >= self.min_frame_len and len(self.data) <= self.max_frame_len