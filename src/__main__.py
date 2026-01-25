import logging
import threading
from typing import Any, Mapping

import matplotlib

from window import Window
from server import SerialServer
from bus import Bus

matplotlib.use("TkAgg")


class ColoredFormatter(logging.Formatter):
    colors = {
        logging.DEBUG: "\033[92m",
        logging.INFO: "\033[0m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: logging.LogRecord):
        base_format = super().format(record)
        color = self.colors.get(record.levelno, "\033[0m")
        return f"{color}{base_format}\033[0m"


handler = logging.StreamHandler()
handler.setFormatter(
    ColoredFormatter(
        datefmt="%H:%M:%S", fmt="[{asctime}] {levelname:<8} - {message}", style="{"
    )
)

logging.basicConfig(level=logging.INFO, handlers=[handler])


bus = Bus()
bus.add_topic("text", str)
bus.add_topic("map", tuple)
bus.add_topic("data", float)

# server = Server(bus)
server = SerialServer(bus)
thread = threading.Thread(target=server.serve)
thread.start()


def on_close():
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
