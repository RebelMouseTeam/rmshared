from dataclasses import dataclass

from content.taxonomy.abc import Condition


@dataclass(frozen=True)
class IsDraft(Condition):
    pass


@dataclass(frozen=True)
class IsPublished(Condition):
    pass


@dataclass(frozen=True)
class IsRemoved(Condition):
    pass
