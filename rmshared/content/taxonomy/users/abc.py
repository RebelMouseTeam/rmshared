from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses


class IAspects(metaclass=ABCMeta):
    @abstractmethod
    def map_user_status(self, type_: consts.USER.STATUS) -> str:
        pass

    @abstractmethod
    def map_user_profile_status(self, status: statuses.Status) -> str:
        pass


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_user_status(self, data: Mapping[str, Any]) -> consts.USER.STATUS:
        pass

    @abstractmethod
    def jsonify_user_status(self, status: consts.USER.STATUS) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def make_user_profile_status(self, data: Mapping[str, Any]) -> statuses.Status:
        pass

    @abstractmethod
    def jsonify_user_profile_status(self, status: statuses.Status) -> Mapping[str, Any]:
        pass
