from abc import ABCMeta
from typing import Callable
from typing import Protocol
from typing import TypeVar

from rmshared.tools import as_is

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.core.aliases import fields

Field = TypeVar('Field', bound=core.fields.Field)
InValue = TypeVar('InValue')
OutValue = TypeVar('OutValue')


class BaseValue(Protocol[Field, InValue, OutValue], metaclass=ABCMeta):
    def __init__(self, field_factory: Callable[..., Field], value_cast_func: Callable[[InValue], OutValue] = as_is):
        self.field_factory = field_factory
        self.value_cast_func = value_cast_func

    def __hash__(self):
        return (self.__class__, self.field_factory).__hash__()


class BaseOther(Protocol[Field], metaclass=ABCMeta):
    def __init__(self, field_factory: Callable[..., Field]):
        self.field_factory = field_factory

    def __hash__(self):
        return (self.__class__, self.field_factory).__hash__()


class SystemFieldValue(BaseValue[fields.System, InValue, OutValue]):
    def __call__(self, value: InValue) -> core.labels.Value[core.fields.System, OutValue]:
        return core.labels.Value(field=self.field_factory(), value=self.value_cast_func(value))


class CustomFieldValue(BaseValue[fields.Custom, InValue, OutValue]):
    def __call__(self, path: str, value: InValue) -> core.labels.Value[core.fields.Custom, OutValue]:
        return core.labels.Value(field=self.field_factory(path=path), value=self.value_cast_func(value))


class SystemFieldBadge(BaseOther[fields.System]):
    def __call__(self) -> core.labels.Badge[core.fields.System]:
        return core.labels.Badge(field=self.field_factory())


class CustomFieldBadge(BaseOther[fields.Custom]):
    def __call__(self, path: str) -> core.labels.Badge[core.fields.Custom]:
        return core.labels.Badge(field=self.field_factory(path))


class SystemFieldEmpty(BaseOther[fields.System]):
    def __call__(self) -> core.labels.Empty[core.fields.System]:
        return core.labels.Empty(field=self.field_factory())


class CustomFieldEmpty(BaseOther[fields.Custom]):
    def __call__(self, path: str) -> core.labels.Empty[core.fields.Custom]:
        return core.labels.Empty(field=self.field_factory(path))
