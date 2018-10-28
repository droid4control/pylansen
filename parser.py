#!/usr/bin/python3

from pylansen.lansendecoder import LansenDecoder
from pylansen.lansen2mbus import Lansen2MBus

import sys
import binascii

import logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

if __name__ == '__main__':
    def cb(buf, rssi, **kwargs):
        log.info('cb({:s}, {:d}, {:s})'.format(str(binascii.hexlify(buf)), rssi, str(kwargs)))

        lmbus = Lansen2MBus()
        try:
            xml = lmbus.getxml(buf)
            print(xml)
        except Exception as ex:
            log.error("got exception %s", ex)

    l = LansenDecoder(sys.stdin.buffer, cb, testarg='test')
    try:
        l.run()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting")
