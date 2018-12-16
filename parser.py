#!/usr/bin/python3

from pylansen.lansendecoder import LansenDecoder
from pylansen.lansen2mbus import Lansen2MBus
from pylansen.enapiversionlong import ENAPIVersionLong
from pylansen.enapimbusmode import ENAPIMbusMode
from pylansen.enapiack import ENAPIAck
from pylansen.enapimbusdata import ENAPIMbusData

import sys
import binascii

import logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

if __name__ == '__main__':
    def cb(timestamp, enapi, **kwargs):
        log.info('cb({:d}, {:s}, {:s})'.format(int(timestamp), str(enapi), str(kwargs)))
        print("wmbus data @{:d}".format(int(timestamp)))

        if isinstance(enapi, ENAPIVersionLong):
            print("got version:", enapi.Version, enapi.Major, enapi.Minor)
        elif isinstance(enapi, ENAPIMbusMode):
            print("input mode", enapi.InputMode)
            print("output mode", enapi.OutputMode)
            print("output frame format", enapi.OutputFrameFormat)
        elif isinstance(enapi, ENAPIAck):
            print("got ACK")
        elif isinstance(enapi, ENAPIMbusData):
            print("got mbus data, RSSI:", enapi.RSSI)
            try:
                lmbus = Lansen2MBus()
                xml = lmbus.getxml(enapi.MbusData)
                print(xml)
            except Exception as ex:
                log.error("got exception %s", ex)
        else:
            print("got unknown data")

    l = LansenDecoder(sys.stdin.buffer, cb, testarg='test')
    try:
        l.run()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting")
