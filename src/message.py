from dataclasses import dataclass
from typing import Tuple

from messagetype import MessageType


@dataclass
class Message:
    datatype: MessageType
    payload: str | float | Tuple[float]
