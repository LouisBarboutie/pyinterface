from typing import Iterable, List

from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import tkinter as tk

from subscriber import Subscriber


class LiveMap(tk.Frame, Subscriber):

    def __init__(self, parent: tk.Misc, title: str) -> None:
        tk.Frame.__init__(self, parent)
        Subscriber.__init__(self, tuple)

        self.figure = Figure()
        self.figure.suptitle(title)
        self.axes = self.figure.subplots()
        self.axes.set_aspect("equal")

        self.map = Basemap(
            llcrnrlon=3,
            llcrnrlat=46,
            urcrnrlon=18,
            urcrnrlat=56,
            ax=self.axes,
            resolution="l",
        )
        self.map.drawcoastlines(linewidth=0.25)
        self.map.drawcountries(linewidth=0.25)

        self.lon_history: List[float] = []
        self.lat_history: List[float] = []
        self.x_history: List[float] = []
        self.y_history: List[float] = []

        self.line = self.axes.plot(self.x_history, self.y_history, marker="o")[0]

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=0)

        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=10,
            cache_frame_data=False,
        )

    def animate(self, frame) -> Iterable[Artist]:
        self.line.set_data(self.x_history, self.y_history)
        return [self.line]

    def handle(self, message: tuple[float, float]) -> None:
        new_lon, new_lat = message
        new_x, new_y = self.map(new_lon, new_lat)
        self.x_history.append(new_x)
        self.y_history.append(new_y)
        self.lon_history.append(new_lon)
        self.lat_history.append(new_lat)
