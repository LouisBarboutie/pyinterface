from collections.abc import Sequence
from enum import IntEnum
from typing import Type


class TopicId(IntEnum):
    TEXT = 0
    GEO_DATA = 1
    ACC_DATA = 2
    GYR_DATA = 3
    MAG_DATA = 4


TOPIC_DATA_TYPES: dict[TopicId, Type] = {
    TopicId.TEXT: str,
    TopicId.GEO_DATA: Sequence,
    TopicId.ACC_DATA: Sequence,
    TopicId.GYR_DATA: Sequence,
    TopicId.MAG_DATA: Sequence,
}
