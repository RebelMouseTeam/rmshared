from rmshared.sql.compiling import compact
from rmshared.sql.compiling.abc import ITree
from rmshared.sql.compiling.bases import Connective


class Conjunction(Connective):
    @property
    def operator(self):
        yield compact.Break()
        yield 'AND'


class Disjunction(Connective):
    @property
    def operator(self):
        yield 'OR'


class Negation(ITree):
    def __init__(self, expression: ITree):
        self.expression = expression

    def compile(self):
        yield 'NOT'
        yield from self.expression.compile()
