import random
import time

from src.application import Application
from src.network.server import Server
from src.pubsub.bus import Bus
from src.pubsub.topictypes import TopicId


class FakeServer(Server):
    def __init__(self, bus: Bus):
        self.bus = bus
        self.should_stop = False

    def serve(self):
        while not self.should_stop:
            self.bus.publish(TopicId.ACC_DATA, [random.random() for _ in range(3)])
            self.bus.publish(TopicId.GYR_DATA, [random.random() for _ in range(3)])
            self.bus.publish(TopicId.MAG_DATA, [random.random() for _ in range(3)])
            time.sleep(0.001)

    def shutdown(self):
        self.should_stop = True


app = Application()
app.stop_server()
server = FakeServer(app.bus)
app.server = server
app.start_server()

app.main()
