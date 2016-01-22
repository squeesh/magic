from enum import Enum, unique


@unique
class Event(Enum):
    TAP = 0
    PLAY = 1
