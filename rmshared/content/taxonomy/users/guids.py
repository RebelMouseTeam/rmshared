from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Guid


@dataclass(frozen=True)
class UserProfile(Guid):
    id: int
