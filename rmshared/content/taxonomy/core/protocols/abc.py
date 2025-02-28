from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import Mapping
from typing import TypeVar

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Value = TypeVar('Value')
Event = TypeVar('Event')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def jsonify_filter(self, filter_: Filter) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_filter(self, data: Mapping[str, Any]) -> Filter:
        ...


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def make_label(self, data: Mapping[str, Any]) -> Label:
        ...

    @abstractmethod
    def jsonify_label(self, label: Label) -> Mapping[str, Any]:
        ...


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def make_range(self, data: Mapping[str, Any]) -> Range:
        ...

    @abstractmethod
    def jsonify_range(self, range_: Range) -> Mapping[str, Any]:
        ...


class IFields(Generic[Field], metaclass=ABCMeta):
    @abstractmethod
    def make_field(self, data: Mapping[str, Any]) -> Field:
        ...

    @abstractmethod
    def jsonify_field(self, field: Field) -> Mapping[str, Any]:
        ...


class IEvents(Generic[Event], metaclass=ABCMeta):
    @abstractmethod
    def make_event(self, data: Mapping[str, Any]) -> Event:
        ...

    @abstractmethod
    def jsonify_event(self, event: Event) -> Mapping[str, Any]:
        ...


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def make_value(self, data: Any) -> Value:
        """
        :raise: ValueError
        """

    @abstractmethod
    def jsonify_value(self, value: Value) -> Any:
        ...


class IComposite(IFilters[Filter], ILabels[Label], IRanges[Range], IFields[Field], IEvents[Event], IValues[Value], metaclass=ABCMeta):
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
