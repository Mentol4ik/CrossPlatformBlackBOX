from enum import Enum


class StatusEnum(str, Enum):
    ABSORBED = "ABSORBED!"
    REFLECTED = "REFLECTED!"
    ESCAPED = "ESCAPED!"
