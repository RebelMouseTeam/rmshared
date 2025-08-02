from abc import ABCMeta
from abc import abstractmethod
from typing import Type

from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.abc import Operator


class IOperators(metaclass=ABCMeta):
    @abstractmethod
    def enter_operator(self, operator: Operator) -> None:
        ...

    @abstractmethod
    def leave_operator(self, operator: Operator) -> None:
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
