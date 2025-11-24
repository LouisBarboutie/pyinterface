import logging
import socketserver
from typing import Dict

from datahandler import DataHandler


class UnknownTelemetryTypeSpecifier(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0].strip()
        socket = self.request[1]

        key, message = data.decode().split(maxsplit=1)
        try:
            message = self.parse(key, message)
            self.server.handlers.get(key).handle(message)
        except Exception as e:
            logging.warning(f"Error while parsing incoming request: {e}")

        print(f"{self.client_address[0]} wrote: ", data, sep="\n")
        socket.sendto(data.upper(), self.client_address)

    def parse(self, key: str, message: str):
        match key:
            case "text":
                return message
            case "map":
                lon, lat = map(float, message.split())
                return (lon, lat)
            case _:
                raise UnknownTelemetryTypeSpecifier(
                    f"Telemetry type specifier '{key}' unknown!"
                )


class Server:
    HOST = "localhost"
    PORT = 9999

    def __init__(self) -> None:
        self.server = socketserver.UDPServer((self.HOST, self.PORT), UDPHandler)
        self.server.handlers: Dict[str, DataHandler] = {}

    def serve(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    def register(self, handler: DataHandler, tag: str):
        self.server.handlers[tag] = handler
