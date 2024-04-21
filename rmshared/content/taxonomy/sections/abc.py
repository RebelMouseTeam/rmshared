from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts


class IAspects(metaclass=ABCMeta):
    @abstractmethod
    def map_section_read_access_kind(self, kind: access.Kind) -> int:
        ...

    @abstractmethod
    def map_section_visibility_status(self, status: consts.VISIBILITY.STATUS) -> str:
        ...


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_section_read_access_kind(self, data: Mapping[str, Any]) -> access.Kind:
        ...

    @abstractmethod
    def jsonify_section_read_access_kind(self, kind: access.Kind) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_section_visibility_status(self, data: Mapping[str, Any]) -> consts.VISIBILITY.STATUS:
        ...

    @abstractmethod
    def jsonify_section_visibility_status(self, status: consts.VISIBILITY.STATUS) -> Mapping[str, Any]:
        ...
