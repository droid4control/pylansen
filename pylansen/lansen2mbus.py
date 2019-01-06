from ctypes import c_char_p, cast, sizeof, addressof, memmove

from mbus.MBus import MBus, MBusFrame
from mbus.MBusDataVariableHeader import MBusDataVariableHeader
from mbus.MBusLowLevel import MBUS_FRAME_LONG_START, MBUS_CONTROL_MASK_RSP_UD, MBUS_CONTROL_INFO_RESP_VARIABLE, MBUS_FRAME_STOP, MBUS_FRAME_TYPE_LONG

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Lansen2MBus(object):
    def __init__(self, libpath=None):
        self._mbus = MBus(host="localhost", port=8888, libpath=libpath)
        self._mbus_frame = MBusFrame()

    def getxml(self, buf):
        _l_field = buf[0]
        log.debug("L-field: %d", _l_field)
        if _l_field != len(buf):
            raise Exception("L-field != length of frame")

        if buf[10] != 0x7a:
            raise Exception("only short frame is supported")

        _d_field = buf[15:]

        self._mbus._libmbus.parse_set_debug(1)

        self._mbus_frame.start1 = MBUS_FRAME_LONG_START
        self._mbus_frame.length1 = len(_d_field) + sizeof(MBusDataVariableHeader) + 3
        self._mbus_frame.length2 = self._mbus_frame.length1
        self._mbus_frame.start2 = self._mbus_frame.start1
        self._mbus_frame.control = MBUS_CONTROL_MASK_RSP_UD
        self._mbus_frame.address = 0x00
        self._mbus_frame.control_information = MBUS_CONTROL_INFO_RESP_VARIABLE
        self._mbus_frame.stop = MBUS_FRAME_STOP
        self._mbus_frame.type = MBUS_FRAME_TYPE_LONG

        header = MBusDataVariableHeader()
        header.id_bcd[0] = buf[4]
        header.id_bcd[1] = buf[5]
        header.id_bcd[2] = buf[6]
        header.id_bcd[3] = buf[7]
        header.manufacturer[0] = buf[2]
        header.manufacturer[1] = buf[3]
        header.version = buf[8]
        header.medium = buf[9]
        header.access_no = buf[11]
        header.status = buf[12]
        header.signature[0] = buf[13]
        header.signature[1] = buf[14]

        memmove(self._mbus_frame.data, addressof(header), sizeof(header))
        self._mbus_frame.data_size = sizeof(MBusDataVariableHeader) + len(_d_field)
        self._mbus_frame.data[12:self._mbus_frame.data_size] = [x for x in _d_field]

        self._mbus_frame.checksum = self._mbus_frame.control + self._mbus_frame.address + self._mbus_frame.control_information
        for i in range(0, self._mbus_frame.data_size):
            self._mbus_frame.checksum += self._mbus_frame.data[i]

        if self._mbus._libmbus.frame_verify(self._mbus_frame):
            raise Exception("mbus verification error: " + str(self._mbus._libmbus.error_str()))

        mbus_frame_data = self._mbus.frame_data_parse(self._mbus_frame)
        xml_result = self._mbus._libmbus.frame_data_xml(mbus_frame_data)
        xml = cast(xml_result, c_char_p).value.decode('ISO-8859-1')
        return xml

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
