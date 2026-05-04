from enum import Enum


class BlockBlastState(Enum):
    START = "start"
    CURRENT = "current"
    NEXT = "next"
    END = "end"
