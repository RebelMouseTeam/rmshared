from typing import Any

from rmshared.content.taxonomy.variables.traversal.visitors.abc import IValues


class Values(IValues):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_constant(self, constant):
        isinstance(self.delegate, IValues) and self.delegate.visit_constant(constant)

    def visit_variable(self, variable):
        isinstance(self.delegate, IValues) and self.delegate.visit_variable(variable)
