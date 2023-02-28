from collections import OrderedDict
from typing import Any
from typing import Callable
from typing import Collection
from typing import ContextManager
from typing import Iterator
from typing import Optional
from typing import TypeVar

from faker.providers import BaseProvider

T = TypeVar('T')


class Provider(BaseProvider):
    def make_random_optional(self, elements: Collection[T], none_probability: Optional[float] = None) -> Optional[T]:
        none_probability = none_probability or 1 / (1 + len(elements))
        element_probability = (1 - none_probability) / len(elements)
        elements = list(map(lambda element: (element, element_probability), elements))
        elements += [(None, none_probability)]
        return self.random_element(elements=OrderedDict(elements))

    def stream_random_items(self, factory_func: Callable[[], T], max_size: int, min_size: int = 1) -> Iterator[T]:
        return map(lambda _: factory_func(), range(self.random_int(max=max_size, min=min_size)))

    def make_object_id_string(self) -> str:
        return self.hexify(text=24 * '^')

    class ContextManager(ContextManager):
        def __init__(self, return_value: Optional[Any] = None):
            self.return_value = return_value

        def __enter__(self):
            return self.return_value or self

        def __exit__(self, __exc_type, __exc_value, __traceback):
            pass
