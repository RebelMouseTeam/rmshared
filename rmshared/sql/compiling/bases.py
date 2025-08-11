from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterator
from collections.abc import Sequence

from rmshared.sql.compiling.abc import ITree


class Connective(ITree, metaclass=ABCMeta):
    def __init__(self, expressions: Sequence[ITree], *, parenthesis: str = ''):
        assert len(expressions) > 0, 'Expressions must not be empty.'
        assert len(parenthesis) in (0, 2), 'Parenthesis must be empty or have two characters.'
        self.expressions = expressions
        self.parenthesis = parenthesis

    def compile(self):
        if len(self.expressions) > 1:
            yield from self.parenthesis[:1]

        yield from self.expressions[0].compile()
        for expression in self.expressions[1:]:
            yield from self.operator
            yield from expression.compile()

        if len(self.expressions) > 1:
            yield from self.parenthesis[-1:]

    @property
    @abstractmethod
    def operator(self) -> Iterator[str]:
        ...
