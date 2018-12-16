from .enapicommand import ENAPICommand
from .exceptions import ENAPILenException, ENAPICrcErrorException

import crcmod

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPICommandWithSvn(ENAPICommand):
    def __init__(self, data):
        super().__init__(data)
        self.Svn = int.from_bytes(self.data[-2:], byteorder='big')
        if not self.is_frame_complete:
            log.debug("incomplete frame: %s", vars(self))
            raise ENAPILenException("data frame is not complete")
        if crcmod.predefined.mkCrcFun("crc-16-en-13757")(self.data[:-2]) != self.Svn:
            raise ENAPICrcErrorException("CRC error")

    @property
    def Svn(self):
        return self._Svn

    @Svn.setter
    def Svn(self, value):
        self._Svn = value
