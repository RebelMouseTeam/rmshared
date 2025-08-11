from rmshared.sql.compiling import compact
from rmshared.sql.compiling.abc import ITree


class CName(ITree):
    def __init__(self, name: str):
        self.name = name

    def compile(self):
        yield self.name


class Keyword(ITree):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def compile(self):
        yield self.keyword.upper()


class String(ITree):
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    def __init__(self, string: str, *, quotes: str = SINGLE_QUOTE):
        self.string = string
        self.quotes = quotes

    def compile(self):
        yield "'{}'".format(self.string.replace(r"'", r"\'"))


class Number(ITree):
    def __init__(self, number: int | float):
        self.number = number

    def compile(self):
        yield str(self.number)


class ItemGetter(ITree):
    def __init__(self, ref: ITree, index: ITree):
        self.ref = ref
        self.index = index

    def compile(self):
        yield from self.ref.compile()
        yield from self.index.compile()


class Nothing(ITree):
    def compile(self):
        return iter(())


class Break(ITree):
    def compile(self):
        yield compact.Break()
