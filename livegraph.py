import logging
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np


class LiveGraph(tk.Frame):

    def __init__(self, parent: tk.Misc, title: str):
        self.parent = parent
        super().__init__(parent)

        self.figure = Figure()
        self.figure.suptitle(title)
        self.axes = self.figure.subplots()
        self.x = np.linspace(0, 10, 25)
        self.y = np.sin(self.x)
        self.line = self.axes.plot(self.x, self.y)[0]
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=10,
            cache_frame_data=False,
        )

        self.graph_frame = tk.Frame(master=self)
        self.button_frame = tk.Frame(master=self)
        self.canvas.get_tk_widget().grid(column=0, row=0)
        self.button_frame.grid(column=1, row=0)

        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.start,
        )
        self.start_button.pack()

        self.stop_button = tk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop,
        )
        self.stop_button.pack()

        self.save_button = tk.Button(
            self.button_frame,
            text="Save",
            command=self.save,
        )
        self.save_button.pack()

    def animate(self, frame):
        self.x += 1
        self.y = np.sin(self.x)
        self.line.set_ydata(self.y)

        return [self.line]

    def start(self):
        self.animation.resume()

    def stop(self):
        self.animation.pause()

    def save(self):
        x = self.line.get_xdata()
        y = self.line.get_ydata()
        logging.info(f"Saving data for LiveGraph: {self.figure.get_suptitle()}")
        logging.info(f"{x=}")
        logging.info(f"{y=}")
