from dataclasses import dataclass

from content.taxonomy.abc import Event


@dataclass(frozen=True)
class PageView(Event):
    pass
