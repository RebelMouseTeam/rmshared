from abc import ABCMeta
from dataclasses import dataclass
from typing import Collection
from typing import Generic
from typing import TypeVar

Label = TypeVar('Label')
Range = TypeVar('Range')


class Filter(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class AnyLabel(Filter, Generic[Label]):
    labels: Collection[Label]


@dataclass(frozen=True)
class NoLabels(Filter, Generic[Label]):
    labels: Collection[Label]


@dataclass(frozen=True)
class AnyRange(Filter, Generic[Range]):
    ranges: Collection[Range]


@dataclass(frozen=True)
class NoRanges(Filter, Generic[Range]):
    ranges: Collection[Range]
