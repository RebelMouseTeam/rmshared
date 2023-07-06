from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.graph import posts
from rmshared.content.taxonomy.graph import users


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_post(self, data: Mapping[str, Any]) -> posts.Post:
        pass

    @abstractmethod
    def jsonify_post(self, post: posts.Post) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def make_user_profile(self, data: Mapping[str, Any]) -> users.UserProfile:
        pass

    @abstractmethod
    def jsonify_user_profile(self, user: users.UserProfile) -> Mapping[str, Any]:
        pass
