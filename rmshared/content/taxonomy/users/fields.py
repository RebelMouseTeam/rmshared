from abc import ABCMeta
from dataclasses import dataclass


class Base(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Title(Base):
    pass


@dataclass(frozen=True)
class LastLoggedInAt(Base):
    pass


@dataclass(frozen=True)
class CustomField(Base):
    path: str
