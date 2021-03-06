from .exceptions import ENAPILenException, ENAPICommandTypeNotImplementedException

import binascii

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

    def __init__(self, buf):
        self._buf = buf
        if len(buf) < self.min_frame_len:
            log.debug("too short frame: %d < %d: %s -> %s", len(buf), self.min_frame_len, buf, vars(self))
            raise ENAPILenException("data frame is too short")
        if len(buf) > self.max_frame_len:
            log.debug("too long frame: %d > %d: %s -> %s", len(buf), self.max_frame_len, buf, vars(self))
            raise ENAPILenException("data frame is too long")
        self.data = None

    def _copy_buf_to_data(self, l):
        if l > len(self.buf):
            log.warning("buf len = %d, need to get %s", len(self.buf), l)
            raise ENAPILenException("data buffer is too short")
        log.debug("buf(%d): %s", len(self.buf), binascii.hexlify(self.buf))
        self.data = self.buf[:l]
        log.debug("data(%d): %s", len(self.data), binascii.hexlify(self.data))
        del self.buf[0:l]
        log.debug("remainig buf(%d): %s", len(self.buf), binascii.hexlify(self.buf))

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def buf(self):
        return self._buf

    @buf.setter
    def buf(self, value):
        self._buf = value

    @property
    def is_frame_len_possible(self):
        return len(self.data) >= self.min_frame_len and len(self.data) <= self.max_frame_len

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
