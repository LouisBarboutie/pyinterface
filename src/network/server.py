from abc import ABC, abstractmethod
import logging
import socketserver
from typing import Optional
import time

import serial

from src.pubsub.bus import Bus
from src.network.codec import Codec, StructCodec


class UnknownTelemetryTypeSpecifier(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0]
        socket = self.request[1]

        if len(data) == self.server.max_packet_size:
            message = f"Received packet has server max packet size, some data might be truncated!"
            logging.warning(message)

        key, message = data.strip().decode().split(maxsplit=1)
        try:
            message = self.parse(key, message)
        except Exception as e:
            logging.warning(f"Error while parsing incoming request: {e}")

        self.server.bus.publish(key, message)

        print(f"{self.client_address[0]} wrote: ", data, sep="\n")
        socket.sendto(data.upper(), self.client_address)

    def parse(self, key: str, message: str):

        match key:
            case "text":
                parsed_message = message
            case "map":
                lon, lat = map(float, message.split())
                parsed_message = (lon, lat)
            case "data":
                return float(message)
            case _:
                raise UnknownTelemetryTypeSpecifier(
                    f"Telemetry type specifier '{key}' unknown!"
                )

        return parsed_message


class Server(ABC):
    codec: Codec = StructCodec()

    def __init__(self, codec: Optional[Codec] = None) -> None:
        if codec is not None:
            Server.codec = codec

    @abstractmethod
    def serve(self): ...

    @abstractmethod
    def shutdown(self): ...


class UDPServer(Server):
    HOST = "localhost"
    PORT = 9999

    def __init__(self, bus: Bus) -> None:
        self.server = socketserver.UDPServer((self.HOST, self.PORT), UDPHandler)
        self.server.bus = bus

    def serve(self):
        logging.info("Starting UDP server...")
        self.server.serve_forever()

    def shutdown(self):
        logging.info("Shutting down UDP server...")
        self.server.shutdown()
        self.server.server_close()


class SerialServer(Server):
    PORT = "/dev/ttyACM0"

    def __init__(self, bus: Bus) -> None:
        self.bus = bus
        self.serial = serial.Serial()
        self.serial.port = self.PORT
        self.should_stop = False
        self.buffer: bytes = b""

    def serve(self) -> None:
        logging.info("Starting serial server...")

        try:
            self.serial.open()
        except serial.SerialException as e:
            logging.error(f"Could not open serial port {self.serial.port}: {e}")
            return

        while not self.should_stop:
            data = self.serial.read_all()  # Non-blocking read

            if not data:
                time.sleep(0.05)
                continue

            self.buffer += data
            logging.info(f"Read {len(data)} bytes into the buffer.")

            if b"\r\n" not in self.buffer:
                logging.warning("Read packet is incomplete")
                continue

            while b"\r\n" in self.buffer:
                length = len(self.buffer)
                message, self.buffer = self.buffer.split(b"\r\n", maxsplit=1)
                decoded = self.codec.decode(message)
                self.bus.publish(decoded["topic"], decoded["data"])
                logging.info(
                    f"Processed {len(message) + 2} out of {length} bytes in the buffer"
                )

    def shutdown(self) -> None:
        logging.info("Shutting down serial server...")
        self.should_stop = True
        self.serial.close()
