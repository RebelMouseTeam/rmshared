from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Generic
from typing import Mapping
from typing import Tuple
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Reference

Case = TypeVar('Case')
Builder = TypeVar('Builder')


class IBuilder(metaclass=ABCMeta):  # TODO: Rename to something better
    @abstractmethod
    def make_operators(self, variables: IVariables) -> IOperators:
        ...

    @abstractmethod
    def make_variables(self) -> IVariables:
        ...

    @abstractmethod
    def make_values(self, variables: IVariables, delegate: core.protocols.IValues) -> core.protocols.IValues:
        ...


class IOperators(Generic[Case], metaclass=ABCMeta):
    @abstractmethod
    def make_operator(self, data: Mapping[str, Any], make_case: Callable[[Any], Case]) -> operators.Operator[Case]:
        ...

    @abstractmethod
    def jsonify_operator(self, operator: operators.Operator, jsonify_case: Callable[[Case], Any]) -> Mapping[str, Any]:
        ...


class IVariables(metaclass=ABCMeta):
    @abstractmethod
    def make_argument(self, data: Any) -> Type[arguments.Argument]:
        ...

    @abstractmethod
    def jsonify_argument(self, argument: Type[arguments.Argument]) -> Any:
        ...

    @abstractmethod
    def make_reference(self, data: Any) -> Reference:
        ...

    @abstractmethod
    def jsonify_reference(self, reference: Reference) -> Mapping[str, Any]:
        ...

    @abstractmethod
    def make_variable(self, data: Any) -> Tuple[Reference, int]:
        ...

    @abstractmethod
    def jsonify_variable(self, reference: Reference, index: int) -> Any:
        ...
