from rmshared.sql.compiling import compact
from rmshared.sql.compiling.logical import Conjunction
from rmshared.sql.compiling.logical import Disjunction
from rmshared.sql.compiling.logical import Negation
from rmshared.sql.compiling.terminals import CName


class TestConjunction:
    def test_single_expression(self):
        expr = CName('condition')
        conjunction = Conjunction([expr])
        result = list(conjunction.compile())
        assert result == ['condition']

    def test_multiple_expressions(self):
        expr1 = CName('condition1')
        expr2 = CName('condition2')
        conjunction = Conjunction([expr1, expr2])

        result = list(conjunction.compile())
        assert result[0] == 'condition1'
        assert isinstance(result[1], compact.Break)
        assert result[2] == 'AND'
        assert result[3] == 'condition2'

    def test_with_parenthesis(self):
        expr1 = CName('a')
        expr2 = CName('b')
        conjunction = Conjunction([expr1, expr2], parenthesis='()')

        result = list(conjunction.compile())
        assert result[0] == '('
        assert result[1] == 'a'
        assert isinstance(result[2], compact.Break)
        assert result[3] == 'AND'
        assert result[4] == 'b'
        assert result[5] == ')'


class TestDisjunction:
    def test_single_expression(self):
        expr = CName('condition')
        disjunction = Disjunction([expr])
        result = list(disjunction.compile())
        assert result == ['condition']

    def test_multiple_expressions(self):
        expr1 = CName('condition1')
        expr2 = CName('condition2')
        disjunction = Disjunction([expr1, expr2])

        result = list(disjunction.compile())
        assert result == ['condition1', 'OR', 'condition2']

    def test_three_expressions(self):
        expr1 = CName('a')
        expr2 = CName('b')
        expr3 = CName('c')
        disjunction = Disjunction([expr1, expr2, expr3])

        result = list(disjunction.compile())
        assert result == ['a', 'OR', 'b', 'OR', 'c']


class TestNegation:
    def test_compile(self):
        expr = CName('condition')
        negation = Negation(expr)
        result = list(negation.compile())
        assert result == ['NOT', 'condition']
