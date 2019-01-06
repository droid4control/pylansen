#!/usr/bin/env python3

from pylansen.lansendecoder import LansenDecoder
from pylansen.lansen2mbus import Lansen2MBus
from pylansen.enapiversionlong import ENAPIVersionLong
from pylansen.enapimbusmode import ENAPIMbusMode
from pylansen.enapiack import ENAPIAck
from pylansen.enapimbusdata import ENAPIMbusData

import sys
import binascii
import serial

import argparse

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

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=str, help='Serial device')
    parser.add_argument('-b', '--baudrate', default=9600, type=int, help='Baudrate')
    args, unknown = parser.parse_known_args()

    if args.port:
        try:
            fd = serial.Serial(port=args.port, baudrate=args.baudrate)
        except serial.serialutil.SerialException as ex:
            log.critical("got exception %s", ex)
            sys.exit(1)
    else:
        fd = sys.stdin.buffer

    l = LansenDecoder(fd, cb, testarg='test')

    try:
        l.run()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
