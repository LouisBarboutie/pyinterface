import logging
from typing import Dict, TypeVar, Generic, Type

from topic import Topic
from subscriber import Subscriber

T = TypeVar("T")


class Bus(Generic[T]):
    """Container for topics."""

    def __init__(self):
        self.topics: Dict[str, Topic[T]] = {}

    def add_topic(self, key: str, message_type: Type[T]) -> None:
        """Registers a new topic on the bus."""
        if key in self.topics.keys():
            logging.warning(f"Topic {key} already registered!")
            return
        self.topics[key] = Topic(message_type)

    def subscribe(self, key: str, subscriber: Subscriber[T]) -> None:
        """Hook up a subscriber to the desired topic."""
        if key not in self.topics.keys():
            logging.warning(
                f"Topic {key} not registered on the bus, couldn't subscribe"
            )
            return
        self.topics[key].subscribe(subscriber)

    def publish(self, key: str, message: T) -> None:
        """Push a message to a topic on the bus."""
        if key not in self.topics.keys():
            logging.warning(f"Topic {key} not registered!")
            return

        topic = self.topics[key]
        if not isinstance(message, topic.type):
            logging.warning(
                f"Type mismatch: topic expects {topic.type}, got {type(message)}"
            )
        topic.publish(message)

    def process(self) -> None:
        """Update all topics to notify their subscribers with the latest messages."""
        for topic in self.topics.values():
            topic.notify()
