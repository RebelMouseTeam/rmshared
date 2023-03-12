from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Mapping
from typing import NoReturn
from typing import Tuple
from typing import Type
from typing import TypeVar

Filter = TypeVar('Filter')
Order = TypeVar('Order')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Value = TypeVar('Value')


class IFilters(Generic[Filter], metaclass=ABCMeta):
    @abstractmethod
    def add_filter(self, filter_type: Type[Filter], protocol: 'IFilters.IProtocol') -> NoReturn:
        pass

    class IProtocol(Generic[Filter], metaclass=ABCMeta):
        @abstractmethod
        def get_keys(self) -> Iterable[str]:
            pass

        @abstractmethod
        def make_filter(self, data: Mapping[str, Any]) -> Filter:
            pass

        @abstractmethod
        def jsonify_filter(self, filter_: Filter) -> Mapping[str, Any]:
            pass


class IOrders(Generic[Order], metaclass=ABCMeta):
    @abstractmethod
    def add_order(self, order_type: Type[Order], protocol: 'IOrders.IProtocol') -> NoReturn:
        pass

    class IProtocol(Generic[Order], metaclass=ABCMeta):
        @abstractmethod
        def get_keys(self) -> Iterable[str]:
            pass

        @abstractmethod
        def make_order(self, data: Mapping[str, Any]) -> Order:
            pass

        @abstractmethod
        def jsonify_order(self, order: Order) -> Mapping[str, Any]:
            pass


class ILabels(Generic[Label], metaclass=ABCMeta):
    @abstractmethod
    def add_label(self, label_type: Type[Label], protocol: 'ILabels.IProtocol') -> NoReturn:
        pass

    class IProtocol(Generic[Label], metaclass=ABCMeta):
        @abstractmethod
        def get_keys(self) -> Iterable[str]:
            pass

        @abstractmethod
        def make_label(self, data: Mapping[str, Any]) -> Label:
            pass

        @abstractmethod
        def jsonify_label(self, label: Label) -> Mapping[str, Any]:
            pass


class IRanges(Generic[Range], metaclass=ABCMeta):
    @abstractmethod
    def add_range(self, range_type: Type[Range], protocol: 'IRanges.IProtocol') -> NoReturn:
        pass

    class IProtocol(Generic[Range], metaclass=ABCMeta):
        @abstractmethod
        def get_keys(self) -> Iterable[str]:
            pass

        @abstractmethod
        def make_range(self, data: Mapping[str, Any]) -> Range:
            pass

        @abstractmethod
        def jsonify_range(self, range_: Range) -> Mapping[str, Any]:
            pass


class IFields(Generic[Field], metaclass=ABCMeta):
    @abstractmethod
    def add_field(self, field_type: Type[Field], protocol: 'IFields.IProtocol') -> NoReturn:
        pass

    class IProtocol(Generic[Field], metaclass=ABCMeta):
        @abstractmethod
        def get_keys(self) -> Iterable[str]:
            pass

        @abstractmethod
        def make_field(self, name: str, info: Mapping[str, Any]) -> Field:
            pass

        @abstractmethod
        def jsonify_field(self, field: Field) -> Tuple[str, Mapping[str, Any]]:
            pass


class IValues(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def add_value(self, protocol: 'IValues.IProtocol[Value]') -> NoReturn:
        pass

    class IProtocol(Generic[Value], metaclass=ABCMeta):
        @abstractmethod
        def get_types(self) -> Iterable[Type[Value]]:
            pass

        @abstractmethod
        def make_value(self, data: Any) -> Value:
            """
            :raises: ValueError
            """

        @abstractmethod
        def jsonify_value(self, value: Value) -> Any:
            pass
