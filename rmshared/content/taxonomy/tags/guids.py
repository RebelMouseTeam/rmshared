from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Guid


@dataclass(frozen=True)
class Tag(Guid):
    slug: str
