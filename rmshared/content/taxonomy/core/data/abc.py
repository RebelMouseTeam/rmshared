from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping

from rmshared.content.taxonomy.core import fields


class IFields(metaclass=ABCMeta):
    @abstractmethod
    def make_field(self, data: Mapping[str, Any]) -> fields.Field:
        pass

    @abstractmethod
    def make_field_data(self, field: fields.Field) -> Mapping[str, Any]:
        pass
