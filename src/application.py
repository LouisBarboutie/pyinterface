import logging
import threading

from src.window import Window
from src.network.server import SerialServer
from src.pubsub.bus import Bus, TopicId


class Application:

    def __init__(self) -> None:
        self.bus = Bus()
        self.bus.add_topic(TopicId.TEXT)
        self.bus.add_topic(TopicId.GEO_DATA)
        self.bus.add_topic(TopicId.ACC_DATA)
        self.bus.add_topic(TopicId.GYR_DATA)
        self.bus.add_topic(TopicId.MAG_DATA)

        # server = Server(bus)
        self.server = SerialServer(self.bus)
        self.start_server()

        self.window = Window()
        self.window.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.bus.subscribe(TopicId.TEXT, self.window.text)
        self.bus.subscribe(TopicId.GEO_DATA, self.window.map)
        self.bus.subscribe(TopicId.ACC_DATA, self.window.graph0)
        self.bus.subscribe(TopicId.GYR_DATA, self.window.graph1)
        self.bus.subscribe(TopicId.MAG_DATA, self.window.graph2)

    def on_close(self):
        self.stop_server()
        self.window.root.destroy()

    def poll_bus(self):
        self.bus.process()
        self.window.root.after(50, self.poll_bus)

    def main(self):
        self.poll_bus()
        self.window.main()

    def start_server(self):
        logging.info("Starting server...")
        self.thread = threading.Thread(target=self.server.serve)
        self.thread.start()

    def stop_server(self):
        logging.info("Stopping server...")
        self.server.shutdown()
        self.thread.join()
