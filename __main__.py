import atexit
import logging
import subprocess

import matplotlib
import tkinter as tk

from livegraph import LiveGraph

matplotlib.use("TkAgg")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[{asctime}] {levelname:<8} - {message}",
    style="{",
    handlers=[logging.StreamHandler()],
)


def start_server() -> subprocess.Popen:
    process = subprocess.Popen(["python", "pyinterface/server.py"])
    logging.info("Started server subprocess")

    # Required to stop the process running in the background after termination
    def cleanup():
        process.kill()
        logging.info("Killed server subprocess")

    atexit.register(cleanup)

    return process


server = start_server()

window = tk.Tk()
window.title("Animation Test")
frame = tk.Frame(window)
frame.grid()

graph0 = LiveGraph(window, "Graph 0")
graph0.grid(column=0, row=0)

graph1 = LiveGraph(window, "Graph 1")
graph1.grid(column=0, row=1)

window.mainloop()
