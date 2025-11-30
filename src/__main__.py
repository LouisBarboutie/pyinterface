import logging
import threading

import matplotlib

from window import Window
from server import Server
from bus import Bus

matplotlib.use("TkAgg")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[{asctime}] {levelname:<8} - {message}",
    style="{",
    handlers=[logging.StreamHandler()],
)

bus = Bus()
bus.add_topic("text", str)
bus.add_topic("map", tuple)
bus.add_topic("data", float)

server = Server(bus)
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

bus.subscribe("text", window.text)
bus.subscribe("map", window.map)
bus.subscribe("data", window.graph0)
bus.subscribe("data", window.graph1)


def poll_bus():
    bus.process()
    window.root.after(50, poll_bus)


poll_bus()
window.main()
