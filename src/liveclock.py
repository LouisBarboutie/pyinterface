from datetime import datetime
import logging
import tkinter as tk


class Clock(tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.label = tk.Entry(master=self)
        self.label.pack()

        self.schedule_synchronise()

    def synchronise(self):
        time = datetime.now()
        self.label.delete(0, tk.END)
        self.label.insert(0, time.strftime("%H:%M:%S"))

    def schedule_synchronise(self):
        self.synchronise()
        self.master.after(1000, self.schedule_synchronise)
