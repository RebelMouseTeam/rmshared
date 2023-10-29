from abc import ABCMeta
from abc import abstractmethod
from typing import AbstractSet
from typing import Generic
from typing import Iterable
from typing import TypeVar

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import filters

Filter = TypeVar('Filter')
Label = TypeVar('Label')
Range = TypeVar('Range')
Field = TypeVar('Field')
Event = TypeVar('Event')
Value = TypeVar('Value')


class IEntity(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def get_values(self, field: fields.Field) -> AbstractSet[Value]:
        pass


class IMatcher(metaclass=ABCMeta):
    @abstractmethod
    def does_entity_match_filters(self, entity: 'IEntity', filters_: Iterable['filters.Filter']) -> bool:
        pass
