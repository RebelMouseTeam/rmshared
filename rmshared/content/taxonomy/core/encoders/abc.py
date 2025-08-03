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
FieldIn = TypeVar('FieldIn')
FieldOut = TypeVar('FieldOut')
EventIn = TypeVar('EventIn')
EventOut = TypeVar('EventOut')
ValueIn = TypeVar('ValueIn')
ValueOut = TypeVar('ValueOut')


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


class IFields(Generic[FieldIn, FieldOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_field(self, field: FieldIn) -> FieldOut:
        ...


class IEvents(Generic[EventIn, EventOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_event(self, event: EventIn) -> EventOut:
        ...


class IValues(Generic[ValueIn, ValueOut], metaclass=ABCMeta):
    @abstractmethod
    def encode_value(self, value: ValueIn) -> ValueOut:
        ...


class IComposite(
    IFilters[FilterIn, FilterOut],
    ILabels[LabelIn, LabelOut],
    IRanges[RangeIn, RangeOut],
    IFields[FieldIn, FieldOut],
    IEvents[EventIn, EventOut],
    IValues[ValueIn, ValueOut],
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
