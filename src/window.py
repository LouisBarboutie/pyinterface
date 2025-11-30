import tkinter as tk

from livegraph import LiveGraph
from livemap import LiveMap
from livetext import LiveText


class Window:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Animation Test")

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.graph0 = LiveGraph(self.root, "Graph 0")
        self.graph0.grid(column=0, row=0)

        self.graph1 = LiveGraph(self.root, "Graph 1")
        self.graph1.grid(column=0, row=1)

        self.map = LiveMap(self.root, "My LiveMap")
        self.map.grid(column=1, row=0)

        self.text = LiveText(self.root)
        self.text.grid(column=1, row=1)

    def main(self):
        self.root.mainloop()
