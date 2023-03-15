from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Mapping

from rmshared.content.taxonomy.core0.abc import Filter
from rmshared.content.taxonomy.core0.abc import Order
from rmshared.content.taxonomy.core0.abc import Field


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_filters(self, data: Iterable[Mapping[str, Any]]) -> Iterator[Filter]:
        pass

    @abstractmethod
    def jsonify_filters(self, filters: Iterable[Filter]) -> Iterator[Mapping[str, Any]]:
        pass

    @abstractmethod
    def make_order(self, data: Mapping[str, Any]) -> Order:
        pass

    @abstractmethod
    def make_field(self, data: Mapping[str, Any]) -> Field:
        pass

    @abstractmethod
    def jsonify_field(self, field: Field) -> Mapping[str, Any]:
        pass