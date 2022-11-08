from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Guid


@dataclass(frozen=True)
class Post(Guid):
    id: int
