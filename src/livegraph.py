from collections import deque
import logging
from typing import List, Deque, Iterable

from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

from subscriber import Subscriber


class LiveGraph(tk.Frame, Subscriber):

    def __init__(self, parent: tk.Misc, title: str):
        tk.Frame.__init__(self, parent)
        Subscriber.__init__(self, float)

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

    def animate(self, frame: int) -> Iterable[Artist]:
        self.line.set_data(self.x_display, self.y_display)

        self.axes.relim()
        self.axes.autoscale_view()

        return [self.line]

    def handle(self, message: float):
        new_x = len(self.x_history)
        new_y = message

        self.x_history.append(new_x)
        self.y_history.append(new_y)

        # Deque takes care of removing the extra elements
        self.x_display.append(new_x)
        self.y_display.append(new_y)
