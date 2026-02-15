import random
import time

from application import Application
from server import Server
from bus import Bus
from topictypes import TopicDataType


class FakeServer(Server):
    def __init__(self, bus: Bus):
        self.bus = bus
        self.should_stop = False

    def serve(self):
        while not self.should_stop:
            self.bus.publish(
                TopicDataType.ACC_DATA, [random.random() for i in range(3)]
            )
            self.bus.publish(
                TopicDataType.GYR_DATA, [random.random() for i in range(3)]
            )
            self.bus.publish(
                TopicDataType.MAG_DATA, [random.random() for i in range(3)]
            )
            time.sleep(0.001)

    def shutdown(self):
        self.should_stop = True


app = Application()
app.stop_server()
server = FakeServer(app.bus)
app.server = server
app.start_server()

app.main()
