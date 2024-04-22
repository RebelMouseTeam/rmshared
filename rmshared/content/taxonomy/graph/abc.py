from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.graph import posts
from rmshared.content.taxonomy.graph import users
from rmshared.content.taxonomy.graph import sections


class IProtocol(metaclass=ABCMeta):
    @abstractmethod
    def make_post(self, data: Mapping[str, Any]) -> posts.Post:
        ...

    @abstractmethod
    def jsonify_post(self, post: posts.Post) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_section(self, data: Mapping[str, Any]) -> sections.Section:
        ...

    @abstractmethod
    def jsonify_section(self, section: sections.Section) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_user_profile(self, data: Mapping[str, Any]) -> users.UserProfile:
        ...

    @abstractmethod
    def jsonify_user_profile(self, user: users.UserProfile) -> Mapping[str, Any]:
        ...
