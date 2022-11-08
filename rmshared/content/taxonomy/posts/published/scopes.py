from abc import ABCMeta
from dataclasses import dataclass


class Scope(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Site(Scope):
    is_promoted: bool


@dataclass(frozen=True)
class Community(Scope):
    is_demoted: bool
