from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, List, Any
from dataclasses import dataclass

from rmshared.typings import CastFunc


class IRequest(metaclass=ABCMeta):
    T = TypeVar('T')

    MISSED = object()
    PAYLOAD = object()

    @abstractmethod
    async def get_argument(self, cast_func: CastFunc[T], path: Union[str, object], default: Union[T, object] = MISSED) -> T:
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
    class ListValue:
        value: List[IRequest.T]

    @abstractmethod
    async def get_argument(self, path: Union[str, object], default: Any) -> Union[Any, ListValue]:
        pass
