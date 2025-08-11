from collections.abc import Callable
from collections.abc import Iterator
from functools import wraps
from itertools import groupby

__all__ = (
    'with_connector',
    'with_indent',
    'with_new_line',
    'with_space',
    'with_comma',
    'with_nothing',

    'Break',
    'breaks_as',
)


def with_connector(connector: str) -> Callable[[Callable[..., Iterator[str]]], Callable[..., Iterator[str]]]:
    def decorator(func: Callable[..., Iterator[str]]) -> Callable[..., Iterator[str]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Iterator[str]:
            for is_break, tokens in groupby(func(*args, **kwargs), key=lambda x: isinstance(x, Break)):
                if is_break:
                    yield from tokens
                else:
                    yield connector.join(tokens)
        return wrapper
    return decorator


with_indent = with_connector(connector='\n    ')
with_new_line = with_connector(connector='\n')
with_space = with_connector(connector=' ')
with_comma = with_connector(connector=', ')
with_nothing = with_connector(connector='')


def breaks_as(replacement: str) -> Callable[[Callable[..., Iterator[str]]], Callable[..., Iterator[str]]]:
    def decorator(func: Callable[..., Iterator[str]]) -> Callable[..., Iterator[str]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Iterator[str]:
            yield ''.join(replacement if isinstance(token, Break) else token for token in func(*args, **kwargs))
        return wrapper
    return decorator


class Break(str):
    def __new__(cls):
        return super().__new__(cls, ' ')
