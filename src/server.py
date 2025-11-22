import socketserver
from typing import Dict

from datahandler import DataHandler


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0].strip()
        socket = self.request[1]
        print(f"{self.client_address[0]} wrote: ", data, sep="\n")
        socket.sendto(data.upper(), self.client_address)


class Server:
    HOST = "localhost"
    PORT = 9999

    def __init__(self) -> None:
        self.server = socketserver.UDPServer((self.HOST, self.PORT), UDPHandler)
        self.handlers: Dict[str, DataHandler] = {}

    def serve(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    def register(self, handler: DataHandler, tag: str):
        self.handlers[tag] = handler
