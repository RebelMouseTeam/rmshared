from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Field(metaclass=ABCMeta):
    name: str


@dataclass(frozen=True)
class System(Field):
    pass


@dataclass(frozen=True)
class Custom(Field):
    path: str
