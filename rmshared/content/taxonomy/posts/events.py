from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Event


@dataclass(frozen=True)
class PageView(Event):
    pass
