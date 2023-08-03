import inspect
from functools import partial

from typing import Any
from typing import Callable
from typing import Generic
from typing import Type

from rmshared.typings import T

from rmshared.content.taxonomy.core import fields


def system_field(name: str) -> Callable[[], 'Alias[fields.System]']:
    def decorator(cls: Type[Any]) -> 'Alias[fields.System]':
        assert inspect.isclass(cls)
        assert inspect.signature(cls.__init__).parameters.keys() == {'self'}
        return Alias(partial(fields.System, name))

    return decorator


def custom_field(name: str) -> Callable[[Type[Any]], 'Alias[fields.Custom]']:
    def decorator(cls: Type[Any]) -> 'Alias[fields.Custom]':
        assert inspect.isclass(cls)
        assert inspect.signature(cls.__init__).parameters.keys() == {'self', 'path'}
        assert inspect.signature(cls.__init__).parameters['path'].annotation is str
        return Alias(partial(fields.Custom, name))

    return decorator


class Alias(Generic[T]):
    def __init__(self, factory: partial):
        self.factory = factory

    def __call__(self, *args, **kwargs) -> T:
        return self.factory(*args, **kwargs)

    def __hash__(self):
        return hash(self.factory)

    def __eq__(self, other):
        return self.factory == other.factory
