from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime
import json
import logging
from struct import Struct
from typing import Dict

from src.network.messagetype import MessageType
from src.pubsub.topictypes import TopicId


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
        MessageType.TEXT: Struct("<BBIB"),  # B = type, B = topic, B = string length
        MessageType.DATA: Struct("<BBIf"),  # B = type, B = topic, f = data value
        MessageType.VEC3: Struct("<BBI3f"),  # B = type, B = topic, 3d = 3 data values
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
        logging.debug(f"Decoding message {message}")
        try:
            message_type = MessageType(message[0])
        except ValueError as e:
            error_message = (
                f"Message type {message[0]} is invalid, message was not decoded: {e}"
            )
            logging.warning(error_message)
            return self.KEYS._make([TopicId.TEXT, str, 0, error_message])._asdict()

        formatter = self.FORMATS[message_type]

        if len(message) != formatter.size:
            error_message = f"Message of length {len(message)} does not match format expected length of {formatter.size} for message of type {message_type.name}"
            logging.error(error_message)
            return self.KEYS._make([TopicId.TEXT, str, 0, error_message])._asdict()

        match message_type:
            case MessageType.TEXT:
                header_length = formatter.size
                _, topic, uptime, payload_length = formatter.unpack(
                    message[:header_length]
                )
                uptime = datetime.fromtimestamp(uptime / 1000).strftime("[%H:%M:%S]")

                if payload_length > len(message) - header_length:
                    error_message = (
                        f"Message header information does not match payload: {message}!"
                    )
                    logging.error(error_message)
                    return self.KEYS._make(
                        [TopicId.TEXT, str, 0, error_message]
                    )._asdict()

                payload = message[
                    header_length : header_length + payload_length
                ].decode()
                logging.info(
                    f"{topic=}, {uptime=}, {payload_length=}, {payload=} {len(payload)=}"
                )
                unpacked = f"{uptime} {payload}"
            case MessageType.DATA:
                _, topic, uptime, unpacked = formatter.unpack(message)
            case MessageType.VEC3:
                _, topic, uptime, x, y, z = formatter.unpack(message)
                unpacked = [x, y, z]

        logging.debug(
            f"Decoded message of type {message_type.name} for topic {TopicId(topic).name}"
        )

        return self.KEYS._make(
            [TopicId(topic), message_type, uptime, unpacked]
        )._asdict()


class JsonCodec(Codec):

    def encode(self, message: dict) -> bytes:
        return json.dumps(message).encode()

    def decode(self, message: bytes) -> dict:
        data = json.loads(message.decode())
        data["type"] = MessageType(data["type"])
        return data
