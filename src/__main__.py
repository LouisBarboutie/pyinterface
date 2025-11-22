import atexit
import logging
import subprocess

import matplotlib
import tkinter as tk

from window import Window

matplotlib.use("TkAgg")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[{asctime}] {levelname:<8} - {message}",
    style="{",
    handlers=[logging.StreamHandler()],
)


def start_server() -> subprocess.Popen:
    process = subprocess.Popen(["python", "src/server.py"])
    logging.info("Started server subprocess")

    # Required to stop the process running in the background after termination
    def cleanup():
        process.kill()
        logging.info("Killed server subprocess")

    atexit.register(cleanup)

    return process


server = start_server()

window = Window()
window.main()
