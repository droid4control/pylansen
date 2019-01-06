from .enapifactory import ENAPIFactory
from .exceptions import ENAPIException

import sys
import time
import crcmod
import binascii

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class LansenDecoder(object):
    def __init__(self, fd=sys.stdin.buffer, cb=None, **kwargs):
        log.info("LansenDecoder()")
        self._fd = fd
        self._cb = cb
        self._cb_args = kwargs
        self._buffer = None
        self._timestamp = None
        self._decode_7d = False

    def run(self):
        log.info("run()")
        while True:
            c = self._fd.read(1)
            if not c:
                log.info("read: EOF")
                return
            log.debug("read: %s", binascii.hexlify(c))
            self._add_byte(c)

    def reset(self):
        log.info("reset()")
        self._buffer = None

    def _add_byte(self, b):
        if b == b'\x7e':
            if self._buffer != None and len(self._buffer):
                log.debug("end marker found")
                self._process_buffer()
            else:
                log.debug("start marker found")
                self._buffer = bytearray()
                self._timestamp = time.time()
        else:
            if self._buffer != None:
                if self._decode_7d:
                    self._decode_7d = False
                    if b == b'\x5e':
                        log.debug("0x7e -> buffer")
                        self._buffer += b'\x7e'
                    elif b == b'\x5d':
                        log.debug("0x7d -> buffer")
                        self._buffer += b'\x7d'
                    else:
                        # 7D followed by unknown byte
                        log.error("7D decode error")
                        self.reset()
                elif b == b'\x7d':
                    self._decode_7d = True
                else:
                    log.debug("%s -> buffer", b)
                    self._buffer += b
            else:
                # in the middle of unknown stream (start byte missing)
                log.debug("skip %s", b)
                pass

    def _process_buffer(self):
        log.info("_process_buffer()")
        while self._buffer:
            log.debug("_buffer: %s", binascii.hexlify(self._buffer))
            try:
                enapi = ENAPIFactory.factory(self._buffer)
                log.debug("ENAPI data: %s: %s", enapi, vars(enapi))
                self._run_cb(enapi)
            except ENAPIException as ex:
                log.warning("frame process error: %s", ex)
                break
        self.reset()

    def _run_cb(self, enapi):
        log.info("run callback function")
        if self._cb:
            self._cb(self._timestamp, enapi, **self._cb_args)


if __name__ == '__main__':
    import binascii

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    def cb(timestamp, enapi, **kwargs):
        print('cb({:d}, {:s}, {:s})'.format(int(timestamp), str(enapi), str(kwargs)))

    l = LansenDecoder(sys.stdin.buffer, cb, testarg='test')
    try:
        l.run()
    except (KeyboardInterrupt, SystemExit) as ex:
        log.info("got exception %s", ex)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
