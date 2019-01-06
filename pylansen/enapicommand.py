from .enapi import ENAPI

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPICommand(ENAPI):
    ENAPI_VERSION_LONG = 0x02
    ENAPI_MBUS_DATA = 0x06
    ENAPI_ACK = 0x11
    ENAPI_MBUS_MODE = 0x14

    def __init__(self, data):
        super().__init__(data)
        self.CommandType = int(data[0])
        self.Len = int(data[1])

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
