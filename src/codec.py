from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
import json
from struct import Struct
from typing import Dict, Callable

from messagetype import MessageType


class DecodeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__()


class Codec(ABC):

    @abstractmethod
    def encode(self, message: dict) -> bytes: ...

    @abstractmethod
    def decode(self, message: bytes) -> dict: ...


class StructCodec(Codec):

    KEYS = namedtuple("DataKeys", ["type", "data"])
    FORMATS: Dict[MessageType, Struct] = {
        MessageType.TEXT: Struct("!BH"),  # B = type, H = string length
        MessageType.DATA: Struct("!Bd"),  # B = type, d = data value
        MessageType.VEC3: Struct("!B3d"),  # B = type, 3d = 3 data values
    }

    def encode(self, message: dict) -> bytes:
        message_type = MessageType(message["type"])
        formatter = self.FORMATS[message_type]

        match message_type:
            case MessageType.TEXT:
                packed = formatter.pack(message_type.value, len(message["data"]))
                packed += message["data"].encode()
            case MessageType.DATA:
                packed = formatter.pack(message_type.value, message["data"])
            case MessageType.VEC3:
                packed = formatter.pack(message_type.value, *message["data"])

        return packed

    def decode(self, message: bytes) -> dict:
        message_type = MessageType(message[0])
        formatter = self.FORMATS[message_type]

        match message_type:
            case MessageType.TEXT:
                _, length = formatter.unpack(message[:3])
                if length > len(message) - 3:
                    raise DecodeError(
                        "Buffer length does not match header specified length"
                    )
                unpacked = message[3 : 3 + length].decode()
            case MessageType.DATA:
                _, unpacked = formatter.unpack(message)
            case MessageType.VEC3:
                _, x, y, z = formatter.unpack(message)
                unpacked = [x, y, z]

        return self.KEYS._make([message_type, unpacked])._asdict()


class JsonCodec(Codec):

    def encode(self, message: dict) -> bytes:
        return json.dumps(message).encode()

    def decode(self, message: bytes) -> dict:
        data = json.loads(message.decode())
        data["type"] = MessageType(data["type"])
        return data
