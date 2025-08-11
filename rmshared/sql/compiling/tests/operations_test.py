from rmshared.sql.compiling.operations import IsTrue
from rmshared.sql.compiling.operations import IsFalse
from rmshared.sql.compiling.operations import IsNull
from rmshared.sql.compiling.operations import IsNotNull
from rmshared.sql.compiling.operations import IsEmpty
from rmshared.sql.compiling.terminals import CName


class TestIsTrue:
    def test_compile(self):
        operand = CName('column')
        operation = IsTrue(operand)

        result = list(operation.compile())
        assert result == ['column', 'IS TRUE']


class TestIsFalse:
    def test_compile(self):
        operand = CName('column')
        operation = IsFalse(operand)

        result = list(operation.compile())
        assert result == ['column', 'IS FALSE']


class TestIsNull:
    def test_compile(self):
        operand = CName('column')
        operation = IsNull(operand)

        result = list(operation.compile())
        assert result == ['column', 'IS NULL']


class TestIsNotNull:
    def test_compile(self):
        operand = CName('column')
        operation = IsNotNull(operand)

        result = list(operation.compile())
        assert result == ['column', 'IS NOT NULL']


class TestIsEmpty:
    def test_compile(self):
        operand = CName('column')
        operation = IsEmpty(operand)

        result = list(operation.compile())
        assert result == ['column', 'IS EMPTY']
