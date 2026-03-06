import tkinter as tk

from src.ui.livegraph import LiveGraph
from src.ui.livemap import LiveMap
from src.ui.livetext import LiveText
from src.ui.menu import Menu
from src.pubsub.topictypes import TopicId, TOPIC_DATA_TYPES


class Window:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Animation Test")

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        data_frame = tk.Frame(self.root)
        info_frame = tk.Frame(self.root)
        data_frame.grid(row=0, column=0)
        info_frame.grid(row=0, column=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        data_frame.grid(sticky="nsew")
        info_frame.grid(sticky="nsew")

        # Widget creation
        self.graph0 = LiveGraph(
            TOPIC_DATA_TYPES[TopicId.ACC_DATA],
            data_frame,
            "Accelerometer",
            ["x", "y", "z"],
            "time [pts]",
            "Acceleration [m/s^2]",
        )
        self.graph1 = LiveGraph(
            TOPIC_DATA_TYPES[TopicId.GYR_DATA],
            data_frame,
            "Gyrometer",
            ["x", "y", "z"],
            "Time [pts]",
            "Angular rate [rad/s]",
        )
        self.graph2 = LiveGraph(
            TOPIC_DATA_TYPES[TopicId.MAG_DATA],
            data_frame,
            "Magnetometer",
            ["x", "y", "z"],
            "Time [pts]",
            "Field strength [Gauss]",
        )
        self.map = LiveMap(TOPIC_DATA_TYPES[TopicId.GEO_DATA], info_frame, "My LiveMap")
        self.text = LiveText(TOPIC_DATA_TYPES[TopicId.TEXT], info_frame)

        # Widget positioning
        self.graph0.grid(column=0, row=0, sticky="nsew")
        self.graph1.grid(column=0, row=1, sticky="nsew")
        self.graph2.grid(column=0, row=2, sticky="nsew")
        self.map.grid(column=0, row=0, sticky="nsew")
        self.text.grid(column=0, row=1, sticky="nsew")

        for row in range(data_frame.grid_size()[1]):
            data_frame.grid_rowconfigure(row, weight=1)

        info_frame.rowconfigure(0, weight=1)
        info_frame.rowconfigure(1, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)

    def main(self):
        self.root.mainloop()
