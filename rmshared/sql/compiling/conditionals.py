from rmshared.sql.compiling.abc import ITree


class ExpressionIfCondition(ITree):
    def __init__(self, condition: ITree, expression: ITree):
        self.condition = condition
        self.expression = expression

    def compile(self):
        yield from self.expression.compile()
        yield 'IF'
        yield from self.condition.compile()


class ExpressionIfConditionOtherwiseExpression(ITree):
    def __init__(self, condition: ITree, true_expression: ITree, else_expression: ITree):
        self.condition = condition
        self.true_expression = true_expression
        self.else_expression = else_expression

    def compile(self):
        yield from self.true_expression.compile()
        yield 'IF'
        yield from self.condition.compile()
        yield 'OTHERWISE'
        yield from self.else_expression.compile()
