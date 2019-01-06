from .enapicommand import ENAPICommand
from .exceptions import ENAPILenException

from enum import Enum

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPIMbusMode(ENAPICommand):
    MIN_FARME_LEN = 7
    MAX_FARME_LEN = 7

    class Mode(Enum):
        S = 0x01
        T = 0x02
        TC = 0x03

    class FrameFormat(Enum):
        A = 0x01
        B = 0x02

    def __init__(self, buf):
        super().__init__(buf)
        if not self.is_frame_complete:
            log.debug("incomplete frame: %s", vars(self))
            raise ENAPILenException("data frame is not complete")
        self.InputMode = ENAPIMbusMode.Mode(self.data[2])
        self.OutputMode = ENAPIMbusMode.Mode(self.data[3])
        self.OutputFrameFormat = ENAPIMbusMode.FrameFormat(self.data[4])

    @property
    def InputMode(self):
        return self._InputMode

    @InputMode.setter
    def InputMode(self, value):
        self._InputMode = value

    @property
    def OutputMode(self):
        return self._OutputMode

    @OutputMode.setter
    def OutputMode(self, value):
        self._OutputMode = value

    @property
    def OutputFrameFormat(self):
        return self._OutputFrameFormat

    @OutputFrameFormat.setter
    def OutputFrameFormat(self, value):
        self._OutputFrameFormat = value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
