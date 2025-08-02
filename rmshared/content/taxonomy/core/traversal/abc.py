from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any
from typing import Generic
from typing import TypeVar

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Event = TypeVar('Event')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def traverse_filters(self, filters_: Iterable[Filter], visitor: Any) -> None:
        ...


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def traverse_labels(self, labels_: Iterable[Label], visitor: Any) -> None:
        ...


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def traverse_ranges(self, ranges_: Iterable[Range], visitor: Any) -> None:
        ...


class IEvents(Generic[Event], metaclass=ABCMeta):
    @abstractmethod
    def traverse_events(self, events_: Iterable[Event], visitor: Any) -> None:
        ...


class IComposite(IFilters[Filter], ILabels[Label], IRanges[Range], IEvents[Event], metaclass=ABCMeta):
    ...


class IAssembler(metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, labels: ILabels, ranges: IRanges) -> IFilters:
        ...

    @abstractmethod
    def make_labels(self) -> ILabels:
        ...

    @abstractmethod
    def make_ranges(self) -> IRanges:
        ...

    @abstractmethod
    def make_events(self) -> IEvents:
        ...
