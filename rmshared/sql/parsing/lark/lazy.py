from functools import cached_property


class LazyGrammar:
    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.filename!r})'

    def __str__(self) -> str:
        return self.content

    def __add__(self, other) -> str:
        return self.content + str(other)

    def __radd__(self, other) -> str:
        return str(other) + self.content

    @cached_property
    def content(self) -> str:
        with open(self.filename, 'r') as file:
            return file.read()
