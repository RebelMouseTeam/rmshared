from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import NoReturn
from typing import Sequence
from typing import Type
from typing import TypeVar

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Value = TypeVar('Value')
Event = TypeVar('Event')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def make_filter(self, data: Mapping[str, Any]) -> Filter:
        pass

    @abstractmethod
    def jsonify_filter(self, filter_: Filter) -> Mapping[str, Any]:
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


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def make_value(self, data: Any) -> Value:
        pass

    @abstractmethod
    def jsonify_value(self, value: Value) -> Any:
        pass


class IBuilder(Generic[Filter, Label, Range, Field, Value], metaclass=ABCMeta):
    Dependency = IFilters | ILabels | IRanges | IFields | IValues

    @abstractmethod
    def customize_filters(self, factory: Callable[..., 'IFilters[Filter]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_labels(self, factory: Callable[..., 'ILabels[Label]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_ranges(self, factory: Callable[..., 'IRanges[Range]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_fields(self, factory: Callable[..., 'IFields[Field]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def customize_values(self, factory: Callable[..., 'IValues[Value]'], dependencies: Sequence[Type['IBuilder.Dependency']]) -> NoReturn:
        pass

    @abstractmethod
    def make_protocol(self) -> 'IProtocol[Filter, Label, Range, Field, Value]':
        pass


class IProtocol(Generic[Filter, Label, Range, Field, Value], metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Filter]:
        pass

    @abstractmethod
    def jsonify_filters(self, filters_: Iterable[Filter]) -> Iterator[Mapping[str, Any]]:
        pass

    @abstractmethod
    def make_filter(self, data: Mapping[str, Any]) -> Filter:
        pass

    @abstractmethod
    def jsonify_filter(self, filter_: Filter) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def make_field(self, data: Mapping[str, Any]) -> Field:
        pass

    @abstractmethod
    def jsonify_field(self, field: Field) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def make_event(self, data: Mapping[str, Any]) -> Event:
        pass

    @abstractmethod
    def jsonify_event(self, event: Event) -> Mapping[str, Any]:
        pass
