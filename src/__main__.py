import logging
import threading

import matplotlib

from window import Window
from server import Server

matplotlib.use("TkAgg")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[{asctime}] {levelname:<8} - {message}",
    style="{",
    handlers=[logging.StreamHandler()],
)

server = Server()
thread = threading.Thread(target=server.serve)
logging.info("Starting server...")
thread.start()


def on_close():
    logging.info("Shutting down server...")
    server.shutdown()
    thread.join()
    window.root.destroy()


window = Window()
window.root.protocol("WM_DELETE_WINDOW", on_close)

server.register(window.text.handler, "text")
server.register(window.map.handler, "map")
server.register(window.graph0.handler, "data")

window.main()
