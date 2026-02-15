import logging
from typing import Dict, Any

from topic import Topic
from topictypes import TopicDataType
from subscriber import Subscriber


class Bus:
    """Container for topics."""

    def __init__(self):
        self.topics: Dict[TopicDataType, Topic] = {}

    def add_topic(self, key: TopicDataType) -> None:
        """Registers a new topic on the bus."""
        if key in self.topics.keys():
            logging.warning(f"Topic {key} already registered!")
            return
        self.topics[key] = Topic(key)
        logging.debug(f"Added topic '{key}' to the message bus")

    def subscribe(self, key: TopicDataType, subscriber: Subscriber[Any]) -> None:
        """Hook up a subscriber to the desired topic."""
        if key not in self.topics.keys():
            logging.warning(
                f"Topic {key} not registered on the bus, couldn't subscribe"
            )
            return
        self.topics[key].subscribe(subscriber)

    def publish(self, key: TopicDataType, message: Any) -> None:
        """Push a message to a topic on the bus."""
        if key not in self.topics.keys():
            logging.warning(f"Topic {key} not registered!")
            return

        topic = self.topics[key]
        if not key == topic.type:
            logging.warning(
                f"Type mismatch: topic '{key}' expects {topic.type}, got {type(message)}"
            )
        topic.publish(message)
        logging.debug(f"Published message '{message}' to topic '{key}'")

    def process(self) -> None:
        """Update all topics to notify their subscribers with the latest messages."""
        for topic in self.topics.values():
            topic.notify()
