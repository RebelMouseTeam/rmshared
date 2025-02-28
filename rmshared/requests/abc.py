from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.typings import CastFunc


class IRequest(metaclass=ABCMeta):
    T = TypeVar('T')

    MISSED = object()
    PAYLOAD = object()

    @abstractmethod
    async def get_argument(self, cast_func: CastFunc[T], path: str | object, default: T | object = MISSED) -> T:
        """
        :raises: IRequest.MissingArgumentException
        :raises: IRequest.InvalidArgumentException
        """

    class MissingArgumentException(LookupError):
        pass

    class InvalidArgumentException(ValueError):
        pass


class IDataAdapter(metaclass=ABCMeta):
    @dataclass(frozen=True)
    class ListValue(Generic[IRequest.T]):
        value: list[IRequest.T]

    @abstractmethod
    async def get_argument(self, path: str | object, default: IRequest.T | object) -> IRequest.T | ListValue[IRequest.T]:
        ...
