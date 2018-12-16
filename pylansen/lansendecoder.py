import sys
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
        else:
            if self._buffer != None:
                if self._decode_7d:
                    self._decode_7d = False
                    if b == b'\x5e':
                        log.debug("0x7e -> buffer", b)
                        self._buffer += b'\x7e'
                    elif b == b'\x5d':
                        log.debug("0x7d -> buffer", b)
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
        log.debug("_buffer: %s", binascii.hexlify(self._buffer))
        if len(self._buffer) < 4:
            log.error("buffer too short")
            return self.reset()
        if self._buffer[0] != 0x06:
            log.error("Lansen MBUS data field missing")
            return self.reset()
        if len(self._buffer) - 2 != self._buffer[1]:
            log.error("buffer len != complete len")
            return self.reset()
        if crcmod.predefined.mkCrcFun("crc-16-en-13757")(self._buffer[:-2]) != int.from_bytes(self._buffer[-2:], byteorder='big'):
            log.error("CRC error")
            return self.reset()
        self._buffer[2] = self._buffer[2] - 1   # remove RSSI byte from L-field
        self._run_cb(self._buffer[2:-3], self._buffer[-3])
        self.reset()

    def _run_cb(self, msg, rssi):
        log.info("run callback function")
        if self._cb:
            self._cb(msg, rssi, **self._cb_args)


if __name__ == '__main__':
    import binascii

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    def cb(buf, rssi, **kwargs):
        print('cb({:s}, {:d}, {:s})'.format(str(binascii.hexlify(buf)), rssi, str(kwargs)))

    l = LansenDecoder(sys.stdin.buffer, cb, testarg='test')
    try:
        l.run()
    except (KeyboardInterrupt, SystemExit) as ex:
        log.info("got exception %s", ex)
