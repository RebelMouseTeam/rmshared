from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

Field = TypeVar('Field')


class Order(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class Value(Order, Generic[Field]):
    field: Field
    reverse: bool
