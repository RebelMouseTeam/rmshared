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
        pass

    @abstractmethod
    def make_filter(self, data: Mapping[str, Any]) -> Filter:
        pass


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def make_label(self, data: Mapping[str, Any]) -> Label:
        pass

    @abstractmethod
    def jsonify_label(self, label: Label) -> Mapping[str, Any]:
        pass


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def make_range(self, data: Mapping[str, Any]) -> Range:
        pass

    @abstractmethod
    def jsonify_range(self, range_: Range) -> Mapping[str, Any]:
        pass


class IFields(Generic[Field], metaclass=ABCMeta):
    @abstractmethod
    def make_field(self, data: Mapping[str, Any]) -> Field:
        pass

    @abstractmethod
    def jsonify_field(self, field: Field) -> Mapping[str, Any]:
        pass


class IEvents(Generic[Event], metaclass=ABCMeta):
    @abstractmethod
    def make_event(self, data: Mapping[str, Any]) -> Event:
        pass

    @abstractmethod
    def jsonify_event(self, event: Event) -> Mapping[str, Any]:
        pass


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def make_value(self, data: Any) -> Value:
        """
        :raise: ValueError
        """

    @abstractmethod
    def jsonify_value(self, value: Value) -> Any:
        pass


class IComposite(IFilters[Filter], ILabels[Label], IRanges[Range], IFields[Field], IEvents[Event], IValues[Value], metaclass=ABCMeta):
    pass


class IBuilder(metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, labels: ILabels, ranges: IRanges) -> IFilters:
        pass

    @abstractmethod
    def make_labels(self, fields: IFields, values: IValues) -> ILabels:
        pass

    @abstractmethod
    def make_ranges(self, fields: IFields, values: IValues) -> IRanges:
        pass

    @abstractmethod
    def make_fields(self) -> IFields:
        pass

    @abstractmethod
    def make_events(self) -> IEvents:
        pass

    @abstractmethod
    def make_values(self) -> IValues:
        pass
