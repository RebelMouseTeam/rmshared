from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator

from rmshared.sql.compiling.abc import ITree
from rmshared.sql.compiling.bases import Connective


class CommaSeparatedList(Connective):
    @property
    def operator(self):
        yield ', '


class CommaSeparatedLines(Connective):
    @property
    def operator(self):
        yield ',\n'


class Wrapped(ITree):
    def __init__(self, delegate: ITree, *, parentheses: str = '()'):
        assert len(parentheses) == 2, 'Parentheses must be a string of length 2'
        self.delegate = delegate
        self.parentheses = parentheses

    def compile(self):
        yield from self.parentheses[:1]
        yield from self.delegate.compile()
        yield from self.parentheses[1:]


class Joined(ITree):
    def __init__(self, delegate: ITree, *, separator: str):
        self.delegate = delegate
        self.separator = separator

    def compile(self):
        yield self.separator.join(self.delegate.compile())


class Chain(ITree):
    @classmethod
    def from_iterable(cls, expressions: Iterable[ITree]):
        return cls(*expressions)

    def __init__(self, *expressions: ITree):
        self.expressions = expressions

    def compile(self):
        for expression in self.expressions:
            yield from expression.compile()


class Compacted(ITree):
    def __init__(self, delegate: ITree, decorator: Callable[[Callable[..., Iterator[str]]], [Callable[..., Iterator[str]]]]):
        self.delegate = delegate
        self.decorator = decorator

    def compile(self):
        return self.decorator(self.delegate.compile)()
