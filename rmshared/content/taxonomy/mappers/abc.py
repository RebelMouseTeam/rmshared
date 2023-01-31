from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Order
from rmshared.content.taxonomy.abc import Field

AnyLabel = TypeVar('AnyLabel', bound=Label)
AnyField = TypeVar('AnyField', bound=Field)


class IFilters(metaclass=ABCMeta):
    def map_filters(self, filters_: Iterable[Filter]) -> Iterator[core.Filter]:
        pass


class ILabels(Generic[AnyLabel], metaclass=ABCMeta):
    @abstractmethod
    def map_label(self, label: AnyLabel) -> core.Label:
        pass


class IRanges(metaclass=ABCMeta):
    @abstractmethod
    def map_range(self, range_: Range) -> Iterator[core.Range]:
        pass


class IOrders(metaclass=ABCMeta):
    @abstractmethod
    def map_order(self, order: Order) -> core.Order:
        pass


class IFields(Generic[AnyField], metaclass=ABCMeta):
    @abstractmethod
    def map_field(self, field: AnyField) -> core.Field:
        pass
