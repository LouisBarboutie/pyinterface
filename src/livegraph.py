from collections import deque
import logging
from typing import List, Deque, Iterable, Sequence

from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

from subscriber import Subscriber


class LiveGraph(tk.Frame, Subscriber[Sequence[float]]):

    def __init__(
        self,
        parent: tk.Misc,
        title: str,
        legend: Sequence[str],
        x_label: str,
        y_label: str,
        dim: int = 3,
    ) -> None:
        tk.Frame.__init__(self, parent)
        Subscriber.__init__(self, Sequence[float])

        self.dimensions = dim

        self.figure = Figure(constrained_layout=True)
        self.figure.suptitle(title)

        # add padding between the labels and figure borders
        self.figure.get_layout_engine().set(w_pad=0.2, h_pad=0.1)

        self.axes = self.figure.subplots()
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

        self.x_history: List[float] = []
        self.y_history: List[List[float]] = [[] for _ in range(dim)]

        self.x_display: Deque[float] = deque(maxlen=25)
        self.y_display: List[Deque[float]] = [deque(maxlen=25) for _ in range(dim)]

        self.lines = [
            self.axes.plot(self.x_display, y, marker="o")[0] for y in self.y_display
        ]
        self.axes.legend(legend, loc="upper left")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")

        # Required for dynamic resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=10,
            cache_frame_data=False,
        )

    def animate(self, frame: int) -> Iterable[Artist]:
        self.canvas.draw_idle()
        for line, data in zip(self.lines, self.y_display):
            line.set_data(self.x_display, data)

        self.axes.relim()
        self.axes.autoscale_view()

        return self.lines

    def handle(self, message: Sequence[float]) -> None:
        if len(message) != self.dimensions:
            logging.error(
                f"Received data with dimension {len(message)}, expected {self.dimensions}"
            )
            return

        new_x = len(self.x_history)
        self.x_history.append(new_x)
        self.x_display.append(new_x)

        for history, display, new in zip(self.y_history, self.y_display, message):
            history.append(new)
            display.append(new)  # deque takes care of removing extra elements
