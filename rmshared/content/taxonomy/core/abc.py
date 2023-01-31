from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar

from rmshared.content.taxonomy.abc import Scalar

T = TypeVar('T')


class Prop(Generic[T], metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(Generic[Scalar]):
    prop: 'Prop'
    value: Scalar


@dataclass(frozen=True)
class Range(Generic[Scalar]):
    prop: 'Prop'
    min_value: Optional[Scalar]
    max_value: Optional[Scalar]
