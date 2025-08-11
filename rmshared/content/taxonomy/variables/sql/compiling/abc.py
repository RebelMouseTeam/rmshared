from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Collection
from typing import Generic
from typing import TypeVar

from rmshared.sql import compiling

O = TypeVar('O')
C = TypeVar('C')
A = TypeVar('A')
R = TypeVar('R')


class IOperators(Generic[O, C], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_operator(self, operator: O, make_tree_from_cases_func: compiling.MakeTreeFunc[Collection[C]]) -> compiling.ITree:
        ...


class IVariables(Generic[R], metaclass=ABCMeta):
    @abstractmethod
    def make_tree_from_reference(self, reference: R) -> compiling.ITree:
        ...


class IComposite(Generic[O, C, R], IOperators[O, C], IVariables[R], metaclass=ABCMeta):
    ...
