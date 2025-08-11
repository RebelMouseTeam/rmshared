from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Set
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.abc import Reference

A = TypeVar('A', bound=Argument)


class IConstraint(metaclass=ABCMeta):
    @abstractmethod
    def validate(self) -> None:
        """
        :raises: rmshared.content.taxonomy.variables.validation.exceptions.ValidationError
        """


class IArguments(metaclass=ABCMeta):
    @abstractmethod
    def get_yields(self, ref: Reference) -> Set[Type[A]]:
        ...
