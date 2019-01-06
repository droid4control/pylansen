from .enapi import ENAPI

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPICommand(ENAPI):
    ENAPI_VERSION_LONG = 0x02
    ENAPI_MBUS_DATA = 0x06
    ENAPI_ACK = 0x11
    ENAPI_MBUS_MODE = 0x14

    def __init__(self, buf):
        super().__init__(buf)
        self.CommandType = ENAPICommand.get_command_type(buf)
        self.Len = ENAPICommand.get_len(buf)

    @property
    def CommandType(self):
        return self._CommandType

    @CommandType.setter
    def CommandType(self, value):
        self._CommandType = value

    @property
    def Len(self):
        return self._Len

    @Len.setter
    def Len(self, value):
        self._Len = value

    @property
    def is_frame_complete(self):
        log.debug("is_frame_complete %d - 2 ? %d", len(self.data), self.Len)
        return len(self.data) - 2 == self.Len

    @staticmethod
    def get_command_type(buf):
        return int(buf[0])

    @staticmethod
    def get_len(buf):
        return int(buf[1])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
