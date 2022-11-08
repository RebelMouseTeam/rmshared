from dataclasses import dataclass

from rmshared.content.taxonomy.abc import Condition


@dataclass(frozen=True)
class IsDraft(Condition):
    pass


@dataclass(frozen=True)
class IsPublished(Condition):
    pass


@dataclass(frozen=True)
class IsRemoved(Condition):
    pass
