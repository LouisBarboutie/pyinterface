import logging
import threading

from window import Window
from server import SerialServer
from bus import Bus, TopicDataType


class Application:

    def __init__(self) -> None:
        self.bus = Bus()
        self.bus.add_topic(TopicDataType.TEXT)
        self.bus.add_topic(TopicDataType.GEO_DATA)
        self.bus.add_topic(TopicDataType.ACC_DATA)
        self.bus.add_topic(TopicDataType.GYR_DATA)
        self.bus.add_topic(TopicDataType.MAG_DATA)

        # server = Server(bus)
        self.server = SerialServer(self.bus)
        self.start_server()

        self.window = Window()
        self.window.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.bus.subscribe(TopicDataType.TEXT, self.window.text)
        self.bus.subscribe(TopicDataType.GEO_DATA, self.window.map)
        self.bus.subscribe(TopicDataType.ACC_DATA, self.window.graph0)
        self.bus.subscribe(TopicDataType.GYR_DATA, self.window.graph1)
        self.bus.subscribe(TopicDataType.MAG_DATA, self.window.graph2)

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
        logging.info("Stopping server...")
        self.thread = threading.Thread(target=self.server.serve)
        self.thread.start()

    def stop_server(self):
        logging.info("Stopping server...")
        self.server.shutdown()
        self.thread.join()
