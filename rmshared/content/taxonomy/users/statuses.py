from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Status(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Pending(Status):
    pass


@dataclass(frozen=True)
class Active(Status):
    pass


@dataclass(frozen=True)
class Inactive(Status):
    is_banned: bool
