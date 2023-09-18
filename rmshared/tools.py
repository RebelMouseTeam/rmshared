from collections import defaultdict
from functools import partial
from itertools import chain
from operator import methodcaller
from typing import Any
from typing import Collection
from typing import Iterator
from typing import Optional
from typing import Tuple
from typing import TypeVar, Callable, Dict, Mapping, Iterable, Sequence, Union, Type

from rmshared.typings import CastFunc

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')
S = TypeVar('S', bound=Sequence)


def as_is(value):
    return value


def apply(func_1: Callable[[Any], T], *funcs) -> Callable[[Any], T]:
    """
    >>> apply(tuple, partial(map, int), partial(str.split, sep=','))('1,2,3')
    (1, 2, 3)
    """
    def func(value: T):
        for func_ in reversed(list(chain([func_1], funcs))):
            value = func_(value)
        return value
    return func


def unless_none(cast_func: Callable[[Any], T], if_none=None) -> Callable[[Any], Optional[T]]:
    """
    >>> unless_none(int, if_none=123)(None)
    123
    >>> unless_none(int, if_none=123)('987')
    987
    >>> unless_none(int, if_none=123)('abc')
    ValueError: invalid literal for int() with base 10: 'abc'
    """
    def func(value):
        if value is None:
            return if_none
        else:
            return cast_func(value)
    return func


def reverse_string(string: str) -> str:
    """
    >>> reverse_string('1,2,3')
    '3,2,1'
    """
    return string[::-1]


def map_sequence(sequence_cast_func: Callable[[Any], Sequence], cast_func: CastFunc[T]) -> Callable[[Any], Sequence[T]]:
    """
    >>> map_sequence(tuple, int)(['1', '2', '3'])
    (1, 2, 3)
    """
    return apply(sequence_cast_func, partial(map, cast_func))


def comma_separated_sequence(sequence_cast_func: Callable[[Any], Sequence[Any]], cast_func: CastFunc[T]) -> Callable[[Any], Sequence[T]]:
    """
    >>> comma_separated_sequence(tuple, int)('1,2,3')
    (1, 2, 3)
    """
    return apply(
        map_sequence(sequence_cast_func, cast_func),
        partial(filter, None),
        partial(map, str.strip),
        partial(str.split, sep=',')
    )


def ensure_map_is_complete(type_class: Type[K], instance_class_to_any_map: T | Mapping[Type[K], Any]) -> T:
    """
    :raise: AssertionError
    """
    subtypes = set(type_class.__subclasses__())
    different_instance_classes = set(instance_class_to_any_map.keys()).symmetric_difference(subtypes)
    different_instance_classes -= {None, type(None)}
    assert not different_instance_classes, different_instance_classes
    return instance_class_to_any_map


def ensure_map_is_likely_complete(type_class: Type[K], any_to_any_map: Mapping[Type[K], V]) -> Mapping[Type[K], V]:
    """
    :raise: AssertionError
    """
    subtypes_count = len(set(type_class.__subclasses__()))
    keys_count = len(set(any_to_any_map.keys()) - {None, type(None)})
    assert subtypes_count == keys_count, any_to_any_map
    return any_to_any_map


class ItemGetter(Callable[[Dict], T]):
    def __init__(self, path: str):
        self.key_list = path.split('.')

    def __call__(self, data: Mapping) -> T:
        """
        :raises: LookupError
        """
        ret = data
        for key in self.key_list:
            ret = ret[key]
        return ret

    def __repr__(self):
        return f'{self.__class__.__name__}({self.key_list})'


class ItemSetter(Callable[[Dict], T]):
    def __init__(self, path):
        self.key_list = path.split('.')

    def __call__(self, data: dict, value: T) -> dict:
        ret = data
        for key in self.key_list[:-1]:
            data.setdefault(key, {})
            data = data[key]

        data[self.key_list[-1]] = value
        return ret


class TheOnlyItemGetter(Callable[[Collection[T]], T]):
    def __init__(self, no_items_found: Type[Exception], too_many_items_found: Type[Exception]):
        self.no_items_found = no_items_found
        self.too_many_items_found = too_many_items_found

    def __call__(self, items: Collection[T]) -> T:
        if len(items) == 1:
            return list(items)[0]
        elif len(items) > 1:
            raise self.too_many_items_found()
        else:
            raise self.no_items_found()


def deep_replace(source: Any, replacement_map: Mapping) -> Mapping:

    def _replace(obj):
        if isinstance(obj, Mapping):
            return map_dict(obj, map_key_func=_replace, map_value_func=_replace)
        elif isinstance(obj, (tuple, list, set, frozenset)):
            return type(obj)(map(_replace, obj))
        try:
            return replacement_map[obj]
        except LookupError:
            return obj

    return _replace(source)


def deep_merge_dicts(dict_1: Mapping, *dict_list) -> dict:
    target = merge_dicts(dict_1, dict_2=dict())
    for source in dict_list:  # type: Mapping
        for key, value in source.items():
            if isinstance(value, Mapping):
                target[key] = deep_merge_dicts(target.get(key, {}), value)
            else:
                target[key] = value
    return target


def merge_dicts(dict_1: Mapping, dict_2: Mapping, *dict_list) -> dict:
    return dict(chain.from_iterable(map(methodcaller('items'), [dict_1, dict_2] + list(dict_list))))


def unique_sequence(sequence):
    seen = set()
    seen_add = seen.add
    return type(sequence)([x for x in sequence if x not in seen and not seen_add(x)])


def align_iterable(iterable: Iterable[T], alignment: Sequence[V], key_func: Union[Type, Callable[[T], V]] = as_is) -> Iterator[T]:
    """
    >>> list(align_iterable([1, 2, 3, 4, 1], [5, 3, 2, 4, 1, 4, 2, 3]))
    [3, 2, 4, 1, 1]
    >>> list(align_iterable([('a', 1), ('b', 1), ('c', 2), ('d', 3), ('e', 3), ('f', 4)], [5, 3, 2, 4, 1, 4, 2, 3], lambda letter_number: letter_number[1]))
    [('d', 3), ('e', 3), ('c', 2), ('f', 4), ('a', 1), ('b', 1)]
    """
    key_to_items_map = group_to_mapping(iterable, key_func=key_func)
    return chain.from_iterable(filter(bool, map(key_to_items_map.get, unique_sequence(alignment))))


def dict_from_list(
        source: Iterable[T],
        key_func: CastFunc[K] = None,
        value_func: CastFunc[V] = None,
        return_type: Type[Mapping[K, V]] = dict
) -> Mapping[K, V]:
    key_iterator = iter(source)
    value_iterator = iter(source)
    return _make_dict(key_iterator, key_func, value_iterator, value_func, return_type)


def invert_dict(source_dict: Mapping[K, V]) -> Mapping[V, K]:
    key_iterator = source_dict.values()
    key_func = None
    value_iterator = source_dict.keys()
    value_func = None
    return _make_dict(key_iterator, key_func, value_iterator, value_func, return_type=type(source_dict))


def map_dict(source_dict: Mapping, map_value_func=None, map_key_func=None, return_type=None):
    key_iterator = source_dict.keys()
    value_iterator = source_dict.values()
    return _make_dict(key_iterator, map_key_func, value_iterator, map_value_func, return_type or type(source_dict))


def _make_dict(key_iterator, key_func, value_iterator, value_func, return_type):
    if key_func is not None:
        key_iterator = map(key_func, key_iterator)
    if value_func is not None:
        value_iterator = map(value_func, value_iterator)
    return return_type(zip(key_iterator, value_iterator))


def filter_dict(source_dict: Mapping[K, V], value_func: Callable[[V], bool]) -> Mapping[K, V]:
    return type(source_dict)(filter(lambda key_value: value_func(key_value[1]), source_dict.items()))


def group_to_mapping(iterable: Iterable[T], key_func: Callable[[T], K], value_func: Callable[[T], V] = as_is, return_type=dict) -> Mapping[K, Sequence[V]]:
    ret = defaultdict(list)
    for item in iterable:
        ret[key_func(item)].append(value_func(item))
    return return_type(ret)


def parse_name_and_info(data: Mapping[str, Any]) -> Tuple[str, Any]:
    if len(data) == 1:
        name = str(list(data.keys())[0])
        info = list(data.values())[0]
        return name, info
    else:
        raise ValueError(['invalid_name_and_info_structure', data])
