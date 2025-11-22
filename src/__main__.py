import logging
import threading

import matplotlib

from window import Window
import server as sv

matplotlib.use("TkAgg")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[{asctime}] {levelname:<8} - {message}",
    style="{",
    handlers=[logging.StreamHandler()],
)

server = sv.server()
thread = threading.Thread(target=server.serve_forever)
thread.start()


def on_close():
    logging.info("Shutting down server...")
    server.shutdown()
    server.server_close()
    thread.join()
    window.root.destroy()


window = Window()
window.root.protocol("WM_DELETE_WINDOW", on_close)
window.main()
