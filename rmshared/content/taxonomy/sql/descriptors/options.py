from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Option(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Id(Option):
    pass


@dataclass(frozen=True)
class Badge(Option):
    pass


@dataclass(frozen=True)
class SingleValue(Option):
    pass


@dataclass(frozen=True)
class MultiValue(Option):
    pass


@dataclass(frozen=True)
class Optional(Option):
    pass


@dataclass(frozen=True)
class Deprecated(Option):
    pass


@dataclass(frozen=True)
class NotSupported(Option):
    pass
