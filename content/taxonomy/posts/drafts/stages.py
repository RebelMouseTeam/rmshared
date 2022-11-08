from abc import ABCMeta
from dataclasses import dataclass


class Stage(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Created(Stage):
    is_imported: bool


@dataclass(frozen=True)
class InProgress(Stage):
    is_rejected: bool


@dataclass(frozen=True)
class InReview(Stage):
    pass


@dataclass(frozen=True)
class Ready(Stage):
    pass
