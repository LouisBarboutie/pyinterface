import logging
from typing import Iterable

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import numpy as np
import tkinter as tk

from datahandler import DataHandler


class LiveMap(tk.Frame):
    def __init__(self, parent: tk.Misc, title: str, handler: DataHandler):
        self.parent = parent
        super().__init__(parent)

        self.handler = handler

        self.figure = Figure()
        self.figure.suptitle(title)
        self.axes = self.figure.subplots()

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

        self.lon_initial = self.map.llcrnrlon
        self.lat_initial = (self.map.latmax + self.map.latmin) / 2
        self.lon = self.lon_initial
        self.lat = self.lat_initial
        x, y = self.map(self.lon_initial, self.lat_initial)
        self.scatter = self.map.scatter(x, y)

        self.x = np.zeros((10,))
        self.y = np.zeros((10,))
        self.line = self.axes.plot(self.x, self.y)[0]

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
            self.lon, self.lat = self.handler.queue.get()
            x, y = self.map(self.lon, self.lat)
            self.x[:-1] = self.x[1:]
            self.y[:-1] = self.y[1:]
            self.x[-1] = x
            self.y[-1] = y

    def animate(self, frame) -> Iterable:

        self.update()
        self.scatter.set_offsets(np.column_stack([self.x, self.y]))
        self.line.set_data(self.x, self.y)

        return [self.scatter, self.line]
