from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Value = TypeVar('Value')
Event = TypeVar('Event')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def enter_filter(self, filter_: Filter) -> None:
        ...

    @abstractmethod
    def leave_filter(self, filter_: Filter) -> None:
        ...


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def enter_label(self, label: Label) -> None:
        ...

    @abstractmethod
    def leave_label(self, label: Label) -> None:
        ...


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def enter_range(self, range_: Range) -> None:
        ...

    @abstractmethod
    def leave_range(self, range_: Range) -> None:
        ...


class IEvents(Generic[Event], metaclass=ABCMeta):
    @abstractmethod
    def enter_event(self, event: Event) -> None:
        ...

    @abstractmethod
    def leave_event(self, event: Event) -> None:
        ...


class IFields(Generic[Field], metaclass=ABCMeta):
    @abstractmethod
    def visit_field(self, field: Field) -> None:
        ...


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def visit_value(self, value: Value) -> None:
        ...
