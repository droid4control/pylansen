from .enapicommandwithsvn import ENAPICommandWithSvn
from .exceptions import ENAPILenException

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPIMbusData(ENAPICommandWithSvn):
    MIN_FARME_LEN = 4

    def __init__(self, buf):
        super().__init__(buf)
        if not self.is_frame_complete:
            log.debug("incomplete frame: %s", vars(self))
            raise ENAPILenException("data frame is not complete")
        self.MbusData = self.data[2:-3]
        self.MbusData[0] -= 1 # remove RSSI byte from L-field
        self.RSSI = int(self.data[-3])

    @property
    def MbusData(self):
        return self._MbusData

    @MbusData.setter
    def MbusData(self, value):
        self._MbusData = value

    @property
    def RSSI(self):
        return self._RSSI

    @RSSI.setter
    def RSSI(self, value):
        self._RSSI = value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
