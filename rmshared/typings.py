from collections.abc import Callable
from copy import copy
from copy import deepcopy
from functools import cached_property
from typing import Any
from typing import Type
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')
CastFunc = Type[T] | Callable[[Any], T]


def read_only(value):
    def _read_only_if_possible(value_):
        try:
            return read_only(value_)
        except NotImplementedError:
            return value_

    if value is None:
        return None
    elif isinstance(value, (bool, int, float, str, tuple, frozenset)):
        return value
    elif isinstance(value, set):
        return frozenset(map(_read_only_if_possible, value))
    elif isinstance(value, list):
        return tuple(map(_read_only_if_possible, value))
    elif isinstance(value, dict):
        return ReadOnlyDict(zip(value.keys(), map(_read_only_if_possible, value.values())))
    else:
        raise NotImplementedError(type(value))


class ReadOnlyDict(dict):  # TODO: consider https://pypi.org/project/frozendict/
    """
    @see: https://stackoverflow.com/questions/19022868/how-to-make-dictionary-read-only-in-python/31049908
    @see: https://stackoverflow.com/questions/1151658/python-hashable-dicts
    """

    def __repr__(self):
        return f'{type(self).__name__}({sorted(self._sorted_items)}'

    def __hash__(self):
        return hash(tuple(self._sorted_items))  # TODO: Consider `frozenset()` instead of `tuple(sorted())`

    @cached_property
    def _sorted_items(self):  # TODO: Seems safe but worth checking in the process
        try:
            return sorted(self.items())
        except TypeError:
            return sorted(map(str, self.items()))

    def __copy__(self):
        return type(self)(copy(list(self.items())))

    def __deepcopy__(self, memo):
        return type(self)(deepcopy(list(self.items()), memo))

    def __reduce__(self):
        return type(self), (list(self.items()), )

    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyDict")

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__
