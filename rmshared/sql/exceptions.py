class InterpreterError(Exception):
    def __init__(self, rule: str, line: int, column: int, original: Exception):
        super().__init__(f'Error at line {line}, column {column} while evaluating "{rule}": {original!s}')
        self.rule = rule
        self.line = line
        self.column = column
        self.original = original
