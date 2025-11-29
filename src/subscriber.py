from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar


T = TypeVar("T")


class Subscriber(ABC, Generic[T]):
    """Interface declaring the required methods to process messages from the bus."""

    def __init__(self, message_type: Type[T]) -> None:
        self.type: Type[T] = message_type

    @abstractmethod
    def handle(self, message: T) -> None:
        """Do something with the message."""
        ...
