from unittest.mock import Mock

from lark import Token
from pytest import fixture

from rmshared.sql.parsing.lark.interpreter import Interpreter


class TestInterpreter:
    @fixture
    def interpreter(self) -> Interpreter:
        return Interpreter()

    def test_string_with_double_quotes(self):
        token = Token('ESCAPED_STRING', '"hello"')
        result = Interpreter.string(token)
        assert result == 'hello'

    def test_string_with_single_quotes(self):
        token = Token('ESCAPED_STRING', "'world'")
        result = Interpreter.string(token)
        assert result == 'world'

    def test_string_with_escaped_quotes(self):
        token = Token('ESCAPED_STRING', r'"hello \"world\""')
        result = Interpreter.string(token)
        assert result == 'hello "world"'

    def test_string_with_escaped_newline(self):
        token = Token('ESCAPED_STRING', '"hello\\nworld"')
        result = Interpreter.string(token)
        assert result == 'hello\nworld'

    def test_number_integer(self):
        token = Token('NUMBER', '42')
        result = Interpreter.number(token)
        assert result == 42
        assert isinstance(result, int)

    def test_number_negative_integer(self):
        token = Token('SIGNED_NUMBER', '-123')
        result = Interpreter.number(token)
        assert result == -123
        assert isinstance(result, int)

    def test_number_float(self):
        token = Token('NUMBER', '3.14')
        result = Interpreter.number(token)
        assert result == 3.14
        assert isinstance(result, float)

    def test_number_negative_float(self):
        token = Token('SIGNED_NUMBER', '-2.5')
        result = Interpreter.number(token)
        assert result == -2.5
        assert isinstance(result, float)

    def test_number_zero(self):
        token = Token('NUMBER', '0')
        result = Interpreter.number(token)
        assert result == 0
        assert isinstance(result, int)

    def test_number_zero_float(self):
        token = Token('NUMBER', '0.0')
        result = Interpreter.number(token)
        assert result == 0.0
        assert isinstance(result, float)

