from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import core0
from rmshared.content.taxonomy.abc import Filter
from rmshared.content.taxonomy.abc import Label
from rmshared.content.taxonomy.abc import Range
from rmshared.content.taxonomy.abc import Order
from rmshared.content.taxonomy.abc import Field

AnyLabel = TypeVar('AnyLabel', bound=Label)
AnyField = TypeVar('AnyField', bound=Field)


class IFilters(metaclass=ABCMeta):
    @abstractmethod
    def map_filters(self, filters_: Iterable[Filter]) -> Iterator[core0.Filter]:
        pass


class ILabels(Generic[AnyLabel], metaclass=ABCMeta):
    @abstractmethod
    def map_label(self, label: AnyLabel) -> core0.Label:
        """
        :raises: LookupError
        """


class IRanges(metaclass=ABCMeta):
    @abstractmethod
    def map_range(self, range_: Range) -> Iterator[core0.Range]:
        """
        :raises: LookupError
        """


class IOrders(metaclass=ABCMeta):
    @abstractmethod
    def map_order(self, order: Order) -> core0.Order:
        pass


class IFields(Generic[AnyField], metaclass=ABCMeta):
    @abstractmethod
    def map_field(self, field: AnyField) -> core0.Field:
        pass
