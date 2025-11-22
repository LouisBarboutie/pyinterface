import tkinter as tk


class LiveText(tk.Frame):

    def __init__(self, parent: tk.Misc):
        self.parent = parent
        super().__init__(parent)

        self.text = tk.Text(master=self)
        self.text.pack()

    def update_text(self, message: str) -> None:
        self.text.insert("end", message)
