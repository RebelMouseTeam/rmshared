from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Order
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Field

AnyFilter = TypeVar('AnyFilter', bound=Filter)
AnyOrder = TypeVar('AnyOrder', bound=Order)
AnyLabel = TypeVar('AnyLabel', bound=Label)
AnyRange = TypeVar('AnyRange', bound=Range)
AnyField = TypeVar('AnyField', bound=Field)


class IFilters(Generic[AnyFilter], metaclass=ABCMeta):
    @abstractmethod
    def map_filters(self, filters_: Iterable[AnyFilter]) -> Iterator[core.filters.Filter]:
        pass


class IOrders(Generic[AnyOrder], metaclass=ABCMeta):
    @abstractmethod
    def map_order(self, order: AnyOrder) -> core.orders.Order:
        pass


class ILabels(Generic[AnyLabel], metaclass=ABCMeta):
    @abstractmethod
    def map_label(self, label: AnyLabel) -> core.labels.Label:
        pass


class IRanges(Generic[AnyRange], metaclass=ABCMeta):
    @abstractmethod
    def map_range(self, range_: AnyRange) -> core.ranges.Range:
        pass


class IFields(Generic[AnyField], metaclass=ABCMeta):
    @abstractmethod
    def map_field(self, field: AnyField) -> core.fields.Field:
        pass
