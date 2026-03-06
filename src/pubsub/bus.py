import logging
from typing import Dict, Any

from src.pubsub.topic import Topic
from src.pubsub.topictypes import TopicId, TOPIC_DATA_TYPES
from src.pubsub.subscriber import Subscriber


class Bus:
    """Container for topics."""

    def __init__(self):
        self.topics: Dict[TopicId, Topic] = {}

    def add_topic(self, key: TopicId) -> None:
        """Registers a new topic on the bus."""
        if key.name in self.topics.keys():
            logging.warning(f"Topic '{key.name}' already registered!")
            return
        self.topics[key] = Topic(TOPIC_DATA_TYPES[key])
        logging.info(f"Added topic '{key.name}' to the message bus")

    def subscribe(self, key: TopicId, subscriber: Subscriber[Any]) -> None:
        """Hook up a subscriber to the desired topic."""
        if key not in self.topics.keys():
            logging.warning(
                f"Topic '{key.name}' not registered on the bus, couldn't subscribe"
            )
            return
        self.topics[key].subscribe(subscriber)

    def publish(self, key: TopicId, message: Any) -> None:
        """Push a message to a topic on the bus."""
        if key not in self.topics.keys():
            logging.warning(
                f"Topic '{key.name}' not registered! Available topics are: {self.topics.keys()}"
            )
            return

        topic = self.topics[key]
        if not TOPIC_DATA_TYPES[key] == topic.type:
            logging.warning(
                f"Type mismatch: topic '{key.name}' expects {topic.type}, got {type(message)}"
            )
        topic.publish(message)
        logging.debug(f"Published message '{message}' to topic '{key.name}'")

    def process(self) -> None:
        """Update all topics to notify their subscribers with the latest messages."""
        for topic in self.topics.values():
            topic.notify()
