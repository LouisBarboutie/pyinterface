from abc import ABC, abstractmethod
from queue import Queue


class DataHandler(ABC):
    def __init__(self):
        self.queue = Queue()

    @abstractmethod
    def handle(self, data: str): ...


class ReplayHandler(DataHandler):
    """Replay the data at the same rate that it was recorded to eg. a .csv file."""

    def handle(self, data: str):
        self.queue.put(data)


class LiveHandler(DataHandler):
    """Use sockets to listen to incoming data from external devices."""

    def handle(self, data: str):
        self.queue.put(data)
