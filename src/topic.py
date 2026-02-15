import logging
from queue import Queue
from typing import Set, Any

from subscriber import Subscriber
from topictypes import TopicDataType


class Topic:
    """Specialized message broker."""

    def __init__(self, message_type: TopicDataType) -> None:
        self.type: type = message_type
        self.subscribers: Set[Subscriber[Any]] = set()
        self.queue: Queue[Any] = Queue()

    def subscribe(self, subscriber: Subscriber[Any]) -> None:
        """Register a new subcriber. Duplicate subscriptions have no effect."""
        if subscriber.type is not self.type:
            logging.warning(
                f"Type mismatch: topic of {self.type} got incompatible subscriber of {subscriber.type}"
            )
            return
        self.subscribers.add(subscriber)

    def publish(self, message: Any) -> None:
        """Publish a message to this topic."""
        # if not isinstance(message, self.type):
        # logging.warning(
        # f"Type mismatch: topic expects messages of {self.type}, got {type(message)}"
        # )
        self.queue.put(message)

    def notify(self) -> None:
        """Notifies the subscribers with all the published messages"""
        while not self.queue.empty():
            message = self.queue.get()
            for subscriber in self.subscribers:
                subscriber.handle(message)
