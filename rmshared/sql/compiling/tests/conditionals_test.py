from rmshared.sql.compiling.conditionals import ExpressionIfCondition
from rmshared.sql.compiling.conditionals import ExpressionIfConditionOtherwiseExpression
from rmshared.sql.compiling.terminals import CName
from rmshared.sql.compiling.terminals import String


class TestExpressionIfCondition:
    def test_compile(self):
        condition = CName('active')
        expression = String('enabled')
        conditional = ExpressionIfCondition(condition, expression)

        result = list(conditional.compile())
        assert result == ["'enabled'", 'IF', 'active']


class TestExpressionIfConditionOtherwiseExpression:
    def test_compile(self):
        condition = CName('status')
        true_expression = String('active')
        else_expression = String('inactive')
        conditional = ExpressionIfConditionOtherwiseExpression(condition, true_expression, else_expression)

        result = list(conditional.compile())
        assert result == ["'active'", 'IF', 'status', 'OTHERWISE', "'inactive'"]
