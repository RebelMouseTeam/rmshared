from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable
from typing import Generic
from typing import TypeVar

Case = TypeVar('Case')
Operator = TypeVar('Operator')


class IOperators(Generic[Operator], metaclass=ABCMeta):
    @abstractmethod
    def traverse_operators(self, operators_: Iterable[Operator], visitor: IVisitor) -> None:
        ...

    class IVisitor(Generic[Case], metaclass=ABCMeta):
        @abstractmethod
        def traverse_cases(self, cases: Iterable[Case]) -> None:
            ...
