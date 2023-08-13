from abc import ABCMeta
from typing import Protocol
from typing import TypeVar

from rmshared.content.taxonomy.core import fields

__all__ = ('System', 'Custom')

Field = TypeVar('Field', bound=fields.Field)


class Base(Protocol[Field], metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return (self.__class__, self.name).__hash__()


class System(Base[fields.System]):
    def __call__(self) -> fields.System:
        return fields.System(name=self.name)


class Custom(Base[fields.Custom]):
    def __call__(self, path: str) -> fields.Custom:
        return fields.Custom(name=self.name, path=path)
