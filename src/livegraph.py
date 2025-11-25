import logging
from collections import deque
from typing import List, Deque

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

from datahandler import DataHandler


class LiveGraph(tk.Frame):

    def __init__(self, parent: tk.Misc, title: str, handler: DataHandler):
        self.parent = parent
        super().__init__(parent)

        self.handler = handler

        self.figure = Figure()
        self.figure.suptitle(title)
        self.axes = self.figure.subplots()

        self.x_history: List[float] = []
        self.y_history: List[float] = []

        self.x_display: Deque[float] = deque(maxlen=25)
        self.y_display: Deque[float] = deque(maxlen=25)

        self.line = self.axes.plot(self.x_display, self.y_display, marker="o")[0]

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=0)

        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=10,
            cache_frame_data=False,
        )

    def update(self) -> None:
        while not self.handler.queue.empty():
            new_x = len(self.x_history)
            new_y = self.handler.queue.get()

            self.x_history.append(new_x)
            self.y_history.append(new_y)

            # Deque takes care of removing the extra elements
            self.x_display.append(new_x)
            self.y_display.append(new_y)

    def animate(self, frame: int):
        self.update()
        self.line.set_data(self.x_display, self.y_display)

        self.axes.relim()
        self.axes.autoscale_view()

        return [self.line]
