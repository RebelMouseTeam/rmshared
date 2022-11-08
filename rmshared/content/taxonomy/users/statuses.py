from abc import ABCMeta
from dataclasses import dataclass


class Status(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Pending(Status):
    pass


@dataclass(frozen=True)
class Active(Status):
    pass


@dataclass(frozen=True)
class Inactive(Status):
    is_banned: bool
