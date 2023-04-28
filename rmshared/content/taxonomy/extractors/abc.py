from abc import ABCMeta
from abc import abstractmethod
from typing import Iterator

from rmshared.content.taxonomy import core


class IValuesExtractor(metaclass=ABCMeta):
    @abstractmethod
    def extract_values(self, field: core.fields.Field) -> Iterator[str | int | float | bool]:
        pass
