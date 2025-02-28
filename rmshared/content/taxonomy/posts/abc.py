from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses


class IAspects(metaclass=ABCMeta):
    @abstractmethod
    def map_post_type(self, type_: consts.POST.TYPE) -> str:
        ...

    @abstractmethod
    def map_post_status(self, status: statuses.Status) -> str:
        ...


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_post_type(self, data: Mapping[str, Any]) -> consts.POST.TYPE:
        ...

    @abstractmethod
    def jsonify_post_type(self, type_: consts.POST.TYPE) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_post_status(self, data: Mapping[str, Any]) -> statuses.Status:
        ...

    @abstractmethod
    def jsonify_post_status(self, status: statuses.Status) -> Mapping[str, Any]:
        ...
