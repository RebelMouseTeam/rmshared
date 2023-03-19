from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Field(metaclass=ABCMeta):
    name: str


@dataclass(frozen=True)
class System(Field):
    pass


@dataclass(frozen=True)
class Custom(Field):  # TODO: consider Custom(name='extras', path='path.to.field') --> Field(name='extras:path.to.field')
    path: str
