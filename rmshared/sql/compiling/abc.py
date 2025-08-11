from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Callable
from collections.abc import Iterator
from typing import TypeAlias
from typing import TypeVar


class ITree(metaclass=ABCMeta):
    @abstractmethod
    def compile(self) -> Iterator[str]:
        ...


T = TypeVar('T')
MakeTreeFunc: TypeAlias = Callable[[T], ITree]
