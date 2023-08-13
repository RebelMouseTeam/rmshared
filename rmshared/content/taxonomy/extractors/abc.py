from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import core

Scalar = TypeVar('Scalar', str, int, float, bool)


class IValuesExtractor(Generic[Scalar], metaclass=ABCMeta):
    @abstractmethod
    def extract_values(self, field: core.fields.Field) -> Iterator[Scalar]:
        pass
