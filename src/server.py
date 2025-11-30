import logging
import socketserver
from typing import Dict

from bus import Bus
from datahandler import DataHandler


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


class Server:
    HOST = "localhost"
    PORT = 9999

    def __init__(self, bus: Bus) -> None:
        self.server = socketserver.UDPServer((self.HOST, self.PORT), UDPHandler)
        self.server.bus = bus

    def serve(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()
