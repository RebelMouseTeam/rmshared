from abc import ABCMeta
from abc import abstractmethod
from typing import AbstractSet
from typing import Generic
from typing import TypeVar

from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import filters

Value = TypeVar('Value')


class IEntity(Generic[Value], metaclass=ABCMeta):
    @abstractmethod
    def get_values(self, field: fields.Field) -> AbstractSet[Value]:
        pass


class IMatcher(metaclass=ABCMeta):
    @abstractmethod
    def does_entity_match_filters(self, entity: 'IEntity', filters_: AbstractSet['filters.Filter']) -> bool:
        pass


"""
TODO: probably just drop it all!

@dataclass(frozen=True)
class Aspects:
    labels: AbstractSet['Label']
    values: AbstractSet['Value']
    extras: Mapping[str, Any]

"""
