from enum import Enum


class ControllerMode(Enum):
    CONFIRM_BEFORE = 0
    NO_CONFIRM = 1
    SLEEP = 2
