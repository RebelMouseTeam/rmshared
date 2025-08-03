from rmshared.content.taxonomy.variables.traversal.visitors.abc import IOperators


class Operators(IOperators):
    def __init__(self, delegate):
        self.delegate = delegate

    def visit_operator(self, operator):
        if isinstance(self.delegate, IOperators):
            return self.delegate.visit_operator(operator)
        else:
            return None
