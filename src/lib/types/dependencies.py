from enum import Enum, auto

class DependencyType(Enum):
    NONE = auto()
    RAW = auto()
    WAR = auto()
    WAW = auto()