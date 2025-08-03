from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Generic
from typing import Optional
from typing import TypeVar

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Value = TypeVar('Value')
Event = TypeVar('Event')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def visit_filter(self, filter_: Filter) -> Optional[AbstractContextManager[None]]:
        ...


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def visit_label(self, label: Label) -> Optional[AbstractContextManager[None]]:
        ...


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def visit_range(self, range_: Range) -> Optional[AbstractContextManager[None]]:
        ...


class IEvents(Generic[Event], metaclass=ABCMeta):
    @abstractmethod
    def visit_event(self, event: Event) -> None:
        ...


class IFields(Generic[Field], metaclass=ABCMeta):
    @abstractmethod
    def visit_field(self, field: Field) -> None:
        ...


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def visit_value(self, value: Value) -> None:
        ...
