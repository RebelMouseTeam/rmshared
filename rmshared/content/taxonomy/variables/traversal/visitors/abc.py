from abc import ABCMeta
from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Optional
from typing import Type

from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.abc import Operator


class IOperators(metaclass=ABCMeta):
    @abstractmethod
    def visit_operator(self, operator: Operator) -> Optional[AbstractContextManager[None]]:
        ...


class IArguments(metaclass=ABCMeta):
    @abstractmethod
    def visit_argument(self, argument: Type[Argument]) -> None:
        ...


class IValues(metaclass=ABCMeta):
    @abstractmethod
    def visit_constant(self, constant: values.Constant) -> None:
        ...

    @abstractmethod
    def visit_variable(self, variable: values.Variable) -> None:
        ...
