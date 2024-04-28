from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

FilterIn = TypeVar('FilterIn')
FilterOut = TypeVar('FilterOut')
LabelIn = TypeVar('LabelIn')
LabelOut = TypeVar('LabelOut')
RangeIn = TypeVar('RangeIn')
RangeOut = TypeVar('RangeOut')
InField = TypeVar('InField')
OutField = TypeVar('OutField')
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')
InEvent = TypeVar('InEvent')
OutEvent = TypeVar('OutEvent')


class IFilters(Generic[FilterIn, FilterOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_filter(self, filter_: FilterIn) -> FilterOut:
        ...


class ILabels(Generic[LabelIn, LabelOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_label(self, label: LabelIn) -> LabelOut:
        ...


class IRanges(Generic[RangeIn, RangeOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_range(self, range_: RangeIn) -> RangeOut:
        ...


class IFields(Generic[InField, OutField], metaclass=ABCMeta):
    @abstractmethod
    def encode_field(self, field: InField) -> OutField:
        ...


class IEvents(Generic[InEvent, OutEvent], metaclass=ABCMeta):
    @abstractmethod
    def encode_event(self, event: InEvent) -> OutEvent:
        ...


class IValues(Generic[InValue, OutValue], metaclass=ABCMeta):
    @abstractmethod
    def encode_value(self, value: InValue) -> OutValue:
        ...


class IComposite(
    IFilters[FilterIn, FilterOut],
    ILabels[LabelIn, LabelOut],
    IRanges[RangeIn, RangeOut],
    IFields[InField, OutField],
    IEvents[InEvent, OutEvent],
    IValues[InValue, OutValue],
    metaclass=ABCMeta
):
    ...


class IBuilder(metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, labels: ILabels, ranges: IRanges) -> IFilters:
        ...

    @abstractmethod
    def make_labels(self, fields: IFields, values: IValues) -> ILabels:
        ...

    @abstractmethod
    def make_ranges(self, fields: IFields, values: IValues) -> IRanges:
        ...

    @abstractmethod
    def make_fields(self) -> IFields:
        ...

    @abstractmethod
    def make_events(self) -> IEvents:
        ...

    @abstractmethod
    def make_values(self) -> IValues:
        ...
