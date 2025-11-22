import tkinter as tk

from livegraph import LiveGraph
from livemap import LiveMap
from livetext import LiveText


class Window:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Animation Test")
        frame = tk.Frame(self.root)
        frame.grid()

        graph0 = LiveGraph(self.root, "Graph 0")
        graph0.grid(column=0, row=0)

        graph1 = LiveGraph(self.root, "Graph 1")
        graph1.grid(column=0, row=1)

        map = LiveMap(self.root, "My LiveMap")
        map.grid(column=1, row=0)

        text = LiveText(self.root)
        text.grid(column=1, row=1)
        text.update_text("Hello Text!")

    def main(self):
        self.root.mainloop()
