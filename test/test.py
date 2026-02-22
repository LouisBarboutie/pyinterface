import tkinter as tk

from src import ui
from src.ui.livegraph import LiveGraph
from src.pubsub.topictypes import TopicDataType
import random

dims: int = 3

root = tk.Tk()
graph = LiveGraph(
    TopicDataType.MAG_DATA,
    root,
    "test",
    ["1", "2", "3"],
    "Field strength [Gauss]",
    "time [pts]",
    dims,
)
graph.pack()


def update_graph():
    data = [random.random() for _ in range(dims)]
    print(f"{data=}")
    graph.handle(data)
    root.after(10, update_graph)


update_graph()

root.mainloop()
