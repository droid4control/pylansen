from .enapicommand import ENAPICommand
from .enapiversionlong import ENAPIVersionLong
from .enapimbusdata import ENAPIMbusData
from .enapiack import ENAPIAck
from .enapimbusmode import ENAPIMbusMode
from .exceptions import ENAPICommandTypeNotImplementedException

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ENAPIFactory(object):
    @staticmethod
    def factory(data):
        enapi = ENAPICommand(data)
        if (enapi.CommandType == ENAPICommand.ENAPI_VERSION_LONG):
            log.debug("found ENAPICommand ENAPI_VERSION_LONG")
            return ENAPIVersionLong(data)
        if (enapi.CommandType == ENAPICommand.ENAPI_MBUS_DATA):
            log.debug("found ENAPICommand ENAPI_MBUS_DATA")
            return ENAPIMbusData(data)
        if (enapi.CommandType == ENAPICommand.ENAPI_ACK):
            log.debug("found ENAPICommand ENAPI_ACK")
            return ENAPIAck(data)
        if (enapi.CommandType == ENAPICommand.ENAPI_MBUS_MODE):
            log.debug("found ENAPICommand ENAPI_MBUS_MODE")
            return ENAPIMbusMode(data)

        raise ENAPICommandTypeNotImplementedException("Unknown CommandType {:d}".format(enapi.CommandType))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
