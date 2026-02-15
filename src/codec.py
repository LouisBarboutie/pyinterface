from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime
import json
import logging
from struct import Struct
from typing import Dict

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

    KEYS = namedtuple("DataKeys", ["topic", "type", "uptime", "data"])
    FORMATS: Dict[MessageType, Struct] = {
        MessageType.TEXT: Struct("<BBBI"),  # B = type, B = topic, B = string length
        MessageType.DATA: Struct("<BBIf"),  # B = type, B = topic, f = data value
        MessageType.VEC3: Struct("<BBI3f"),  # B = type, B = topic, 3d = 3 data values
    }
    TOPICS = ["text", "map", "data"]

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
        try:
            message_type = MessageType(message[0])
        except ValueError as e:
            logging.warning(
                f"Message type {message[0]} is invalid, message was not decoded: {e}"
            )
            return self.KEYS._make([None, None, None])._asdict()

        formatter = self.FORMATS[message_type]

        match message_type:
            case MessageType.TEXT:
                header_length = formatter.size
                _, topic, payload_length, uptime = formatter.unpack(
                    message[:header_length]
                )
                unpacked = (
                    datetime.fromtimestamp(uptime / 1000).strftime("[%H:%M:%S]")
                    + message[header_length : header_length + payload_length].decode()
                )
            case MessageType.DATA:
                _, topic, uptime, unpacked = formatter.unpack(message)
            case MessageType.VEC3:
                _, topic, uptime, x, y, z = formatter.unpack(message)
                unpacked = [x, y, z]

        return self.KEYS._make(
            [self.TOPICS[topic], message_type, uptime, unpacked]
        )._asdict()


class JsonCodec(Codec):

    def encode(self, message: dict) -> bytes:
        return json.dumps(message).encode()

    def decode(self, message: bytes) -> dict:
        data = json.loads(message.decode())
        data["type"] = MessageType(data["type"])
        return data
