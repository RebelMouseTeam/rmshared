from rmshared.sql.compiling.abc import ITree


class Function(ITree):
    def __init__(self, name: ITree, args: ITree):
        self.name = name
        self.args = args

    def compile(self):
        yield from self.name.compile()
        yield '('
        yield from self.args.compile()
        yield ')'
