import tkinter as tk

from subscriber import Subscriber


class LiveText(tk.Frame, Subscriber):

    def __init__(self, parent: tk.Misc):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        Subscriber.__init__(self, str)

        self.text = tk.Text(master=self)
        self.text.pack()

    def handle(self, message: str):
        self.text.insert("end", f"Received: {message}\n")
        self.text.see("end")
