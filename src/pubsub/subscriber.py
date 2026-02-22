from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from src.pubsub.topictypes import TopicDataType

T = TypeVar("T")


class Subscriber(ABC, Generic[T]):
    """Interface declaring the required methods to process messages from the bus."""

    def __init__(self, message_type: TopicDataType) -> None:
        self.type = message_type

    @abstractmethod
    def handle(self, message: Type[T]) -> None:
        """Do something with the message."""
        ...
