import logging
import socketserver


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0].strip()
        socket = self.request[1]
        print(f"{self.client_address[0]} wrote: ", data, sep="\n")
        socket.sendto(data.upper(), self.client_address)


def server() -> socketserver.UDPServer:
    logging.info("Started server subprocess")
    HOST, PORT = "localhost", 9999
    return socketserver.UDPServer((HOST, PORT), UDPHandler)
