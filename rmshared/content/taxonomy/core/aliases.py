from abc import ABCMeta
from typing import Protocol
from typing import TypeVar

from rmshared.content.taxonomy.core import fields

F = TypeVar('F', bound=fields.Field)


def system_field(name: str) -> 'SystemFieldAlias':
    return SystemFieldAlias(name)


def custom_field(name: str) -> 'CustomFieldAlias':
    return CustomFieldAlias(name)


class Field(Protocol[F], metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return (self.__class__, self.name).__hash__()


class SystemFieldAlias(Field[fields.System]):
    def __call__(self) -> fields.System:
        return fields.System(name=self.name)


class CustomFieldAlias(Field[fields.Custom]):
    def __call__(self, path: str) -> fields.Custom:
        return fields.Custom(name=self.name, path=path)
