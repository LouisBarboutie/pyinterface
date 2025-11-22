from typing import Iterable

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import numpy as np
import tkinter as tk


class LiveMap(tk.Frame):
    def __init__(self, parent: tk.Misc, title: str):
        super().__init__(parent)

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

        self.xc_offset = 0
        self.lon_initial = self.map.llcrnrlon
        self.lat_initial = (self.map.latmax + self.map.latmin) / 2
        x, y = self.map(self.lon_initial, self.lat_initial)
        self.scatter = self.map.scatter(x, y)

        self.x = np.zeros((30,))
        self.y = np.zeros((30,))
        self.line = self.axes.plot(self.x, self.y)[0]

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=0)

        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=10,
            cache_frame_data=False,
        )

    def animate(self, frame) -> Iterable:

        xc_offset = frame / 10
        xc_offset %= self.map.lonmax - self.map.lonmin

        lon = self.lon_initial + np.cos(frame)
        lat = self.lat_initial + np.sin(frame)
        lon += xc_offset
        x, y = self.map(lon, lat)

        self.x[:-1] = self.x[1:]
        self.y[:-1] = self.y[1:]
        self.x[-1] = x
        self.y[-1] = y

        self.scatter.set_offsets([x, y])
        self.line.set_data(self.x, self.y)

        return [self.scatter, self.line]
