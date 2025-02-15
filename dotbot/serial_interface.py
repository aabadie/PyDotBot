"""Dotbot controller serial interface."""

import threading
import time

from typing import Callable

import serial

from dotbot.logger import LOGGER


PAYLOAD_CHUNK_SIZE = 64
PAYLOAD_CHUNK_DELAY = 0.002  # 2 ms


class SerialInterfaceException(Exception):
    """Exception raised when serial port is disconnected."""


class SerialInterface(threading.Thread):
    """Bidirectional serial interface."""

    def __init__(self, port: str, baudrate: int, callback: Callable):
        self.callback = callback
        self.serial = serial.Serial(port, baudrate)
        super().__init__(daemon=True)
        self.start()
        self._logger = LOGGER.bind(context=__name__)
        self._logger.info("Serial port thread started")

    def run(self):
        """Listen continuously at each byte received on serial."""
        try:
            while 1:
                byte = self.serial.read(1)
                if byte is None:
                    msg = "Serial port disconnected"
                    self._logger.warning(msg)
                    raise SerialInterfaceException(msg)
                self.callback(byte)
        except serial.serialutil.PortNotOpenError as exc:
            self._logger.error(f"{exc}")
            raise SerialInterfaceException(f"{exc}") from exc
        except serial.serialutil.SerialException as exc:
            self._logger.error(f"{exc}")
            raise SerialInterfaceException(f"{exc}") from exc

    def write(self, bytes_):
        """Write bytes on serial."""
        # Send 64 bytes at a time
        pos = 0
        while (pos % PAYLOAD_CHUNK_SIZE) == 0 and pos < len(bytes_):
            self.serial.write(bytes_[pos : pos + PAYLOAD_CHUNK_SIZE])
            self.serial.flush()
            pos += PAYLOAD_CHUNK_SIZE
            time.sleep(PAYLOAD_CHUNK_DELAY)
