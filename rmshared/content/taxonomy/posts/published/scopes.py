from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Scope(metaclass=ABCMeta):
    ...


@dataclass(frozen=True)
class Site(Scope):
    is_promoted: bool


@dataclass(frozen=True)
class Community(Scope):
    is_demoted: bool
