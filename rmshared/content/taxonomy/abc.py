from abc import ABCMeta
from dataclasses import dataclass

from rmshared.dataclasses import total_ordering


@dataclass(frozen=True)
@total_ordering
class Guid(metaclass=ABCMeta):
    pass
