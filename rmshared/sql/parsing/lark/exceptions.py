class ParserError(Exception):
    def __init__(self, line: int, column: int, context: str, original: Exception):
        super().__init__(f'Error at line {line}, column {column}: {original!s}')
        self.line = line
        self.column = column
        self.context = context
        self.original = original


class InterpreterError(Exception):
    def __init__(self, rule: str, line: int, column: int, original: Exception):
        super().__init__(f'Error at line {line}, column {column} while evaluating "{rule}": {original!s}')
        self.rule = rule
        self.line = line
        self.column = column
        self.original = original
