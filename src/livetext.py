import tkinter as tk

from datahandler import DataHandler


class LiveText(tk.Frame):

    def __init__(self, parent: tk.Misc, handler: DataHandler):
        self.parent = parent
        super().__init__(parent)

        self.handler = handler

        self.text = tk.Text(master=self)
        self.text.pack()

        self.update()

    def update(self) -> None:
        while not self.handler.queue.empty():
            message = self.handler.queue.get()
            self.text.insert("end", f"Received: {message}\n")
            self.text.see("end")

        # Schedule the next update
        self.after(100, self.update)
