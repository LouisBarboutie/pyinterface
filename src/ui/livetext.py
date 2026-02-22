import logging

import tkinter as tk

from src.pubsub.subscriber import Subscriber
from src.pubsub.topictypes import TopicDataType


class LiveText(tk.Frame, Subscriber):

    def __init__(self, topic_type: TopicDataType, parent: tk.Misc):
        self.parent = parent
        tk.Frame.__init__(self, parent, bg="white")
        Subscriber.__init__(self, topic_type)

        self.text = tk.Text(master=self, relief="solid", borderwidth=1)
        self.text.pack(expand=True, fill="both", padx=10, pady=10)

    def handle(self, message: str):
        logging.debug(f"Received message {message}")
        self.text.insert("end", f"{message}\n")
        self.text.see("end")
