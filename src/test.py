import tkinter as tk
from livegraph import LiveGraph
import random

dims: int = 3

root = tk.Tk()
graph = LiveGraph(
    root, "test", ["1", "2", "3"], "Field strength [Gauss]", "time [pts]", dims
)
graph.pack()


def update_graph():
    data = [random.random() for _ in range(dims)]
    print(f"{data=}")
    graph.handle(data)
    root.after(10, update_graph)


update_graph()

root.mainloop()
