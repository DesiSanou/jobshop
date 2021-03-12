from enum import Enum
from jobshop.Schedule import Schedule
from jobshop.Instance import Instance


class ExitCause(Enum):
    Timeout = 0
    ProvedOptimal = 1
    Blocked = 2


class Result:
    def __init__(self, instance: Instance, schedule: Schedule, cause: ExitCause):
        self.instance = instance
        self.schedule = schedule
        self.ExitCause = cause