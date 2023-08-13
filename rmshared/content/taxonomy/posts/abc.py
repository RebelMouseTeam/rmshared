from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.posts import consts
from rmshared.content.taxonomy.posts import statuses


class IAspects(metaclass=ABCMeta):
    @abstractmethod
    def map_post_type(self, type_: consts.POST.TYPE) -> str:
        pass

    @abstractmethod
    def map_post_status(self, status: statuses.Status) -> str:
        pass


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_post_type(self, data: Mapping[str, Any]) -> consts.POST.TYPE:
        pass

    @abstractmethod
    def jsonify_post_type(self, type_: consts.POST.TYPE) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def make_post_status(self, data: Mapping[str, Any]) -> statuses.Status:
        pass

    @abstractmethod
    def jsonify_post_status(self, status: statuses.Status) -> Mapping[str, Any]:
        pass
