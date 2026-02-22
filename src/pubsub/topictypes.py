from collections.abc import Sequence
from enum import Enum
from typing import Type
from dataclasses import dataclass


@dataclass(frozen=True)
class TopicInfo:
    id: int
    type: Type


class TopicDataType(Enum):
    TEXT = TopicInfo(0, str)
    GEO_DATA = TopicInfo(1, Sequence)
    ACC_DATA = TopicInfo(2, Sequence)
    GYR_DATA = TopicInfo(3, Sequence)
    MAG_DATA = TopicInfo(4, Sequence)
