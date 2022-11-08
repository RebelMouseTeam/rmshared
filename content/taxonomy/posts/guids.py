from dataclasses import dataclass

from content.taxonomy.abc import Guid


@dataclass(frozen=True)
class Post(Guid):
    id: int
