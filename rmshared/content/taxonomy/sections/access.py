from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Kind(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Public(Kind):
    pass


@dataclass(frozen=True)
class Restricted(Kind):
    is_inherited: bool
