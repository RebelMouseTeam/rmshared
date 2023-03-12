from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import NoReturn
from typing import Sequence
from typing import Type
from typing import TypeVar

InFilter = TypeVar('InFilter')
OutFilter = TypeVar('OutFilter')
InOrder = TypeVar('InOrder')
OutOrder = TypeVar('OutOrder')
InLabel = TypeVar('InLabel')
OutLabel = TypeVar('OutLabel')
InRange = TypeVar('InRange')
OutRange = TypeVar('OutRange')
InField = TypeVar('InField')
OutField = TypeVar('OutField')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class IFilters(Generic[InFilter, OutFilter], metaclass=ABCMeta):
    @abstractmethod
    def visit_filter(self, filter_: InFilter) -> OutFilter:
        pass


class IOrders(Generic[InOrder, OutOrder], metaclass=ABCMeta):
    @abstractmethod
    def visit_order(self, order: InOrder) -> OutOrder:
        pass


class ILabels(Generic[InLabel, OutLabel], metaclass=ABCMeta):
    @abstractmethod
    def visit_label(self, label: InLabel) -> OutLabel:
        pass


class IRanges(Generic[InRange, OutRange], metaclass=ABCMeta):
    @abstractmethod
    def visit_range(self, range_: InRange) -> OutRange:
        pass


class IFields(Generic[InField, OutField], metaclass=ABCMeta):
    @abstractmethod
    def visit_field(self, field: InField) -> OutField:
        pass


class IValues(Generic[InValue, OutValue], metaclass=ABCMeta):
    @abstractmethod
    def visit_value(self, value: InValue) -> OutValue:
        pass


class IBuilder(Generic[InFilter, OutFilter, InLabel, OutLabel, InRange, OutRange, InField, OutField, InValue, OutValue], metaclass=ABCMeta):
    Dependency = IFilters | IOrders | ILabels | IRanges | IFields | IValues

    @abstractmethod
    def customize_filters(self, factory: Callable[..., 'IFilters[InFilter, OutFilter]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_orders(self, factory: Callable[..., 'IOrders[InOrder, OutOrder]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_labels(self, factory: Callable[..., 'ILabels[InLabel, OutLabel]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_ranges(self, factory: Callable[..., 'IRanges[InRange, OutRange]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_fields(self, factory: Callable[..., 'IFields[InField, OutField]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_values(self, factory: Callable[..., 'IValues[InValue, OutValue]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def make_visitor(self) -> 'IVisitor[InFilter, OutFilter, InLabel, OutLabel, InRange, OutRange, InField, OutField, InValue, OutValue]':
        pass


class IVisitor(Generic[InFilter, OutFilter, InLabel, OutLabel, InRange, OutRange, InField, OutField, InValue, OutValue], metaclass=ABCMeta):
    @abstractmethod
    def visit_filters(self, filters: Iterable[InFilter]) -> Iterator[OutFilter]:
        pass

    @abstractmethod
    def visit_order(self, order: InOrder) -> OutOrder:
        pass
