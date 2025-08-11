from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable
from typing import Type
from typing import TypeVar

from rmshared.content.taxonomy.sql.descriptors import scopes
from rmshared.content.taxonomy.sql.descriptors.beans import Descriptor

T = TypeVar('T')


class IRegistry(metaclass=ABCMeta):
    @abstractmethod
    def get_descriptor(self, subject: T) -> Descriptor[T]:
        ...

    @abstractmethod
    def find_descriptor(self, alias: str, scope: scopes.Scope, subject_type: Type[T]) -> Descriptor[T]:
        ...

    @abstractmethod
    def find_all(self, subject_type: Type[T]) -> Iterable[Descriptor[T]]:
        ...
