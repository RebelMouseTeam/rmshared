class InterpreterError(Exception):
    def __init__(self, rule: str, line: int, column: int, end_line: int, end_column: int, original: Exception):
        super().__init__(f'Error at line {line}, column {column} while evaluating "{rule}": {original!s}')
        self.rule = rule
        self.line = line
        self.column = column
        self.end_line = end_line
        self.end_column = end_column
        self.original = original
