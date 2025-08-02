from rmshared.content.taxonomy.variables.traversal.visitors.abc import IOperators


class Operators(IOperators):
    def __init__(self, delegate):
        self.delegate = delegate

    def enter_operator(self, operator):
        isinstance(self.delegate, IOperators) and self.delegate.enter_operator(operator)

    def leave_operator(self, operator):
        isinstance(self.delegate, IOperators) and self.delegate.leave_operator(operator)
