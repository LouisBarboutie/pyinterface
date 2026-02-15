import tkinter as tk


class Menu:
    def __init__(self, master: tk.Misc) -> None:
        self.master = master

        self.menu = tk.Menu(self.master)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Save log as", command=None)
        self.menu.add_cascade(label="File", menu=file_menu)

        data_menu = tk.Menu(self.menu, tearoff=0)
        data_menu.add_command(label="Start acquisition", command=None)
        data_menu.add_command(label="Stop acquisition", command=None)
        self.menu.add_cascade(label="Data", menu=data_menu)

        network_menu = tk.Menu(self.menu, tearoff=0)
        network_menu.add_command(label="Start server", command=None)
        network_menu.add_command(label="Stop server", command=None)
        network_menu.add_command(label="Select encoding", command=None)
