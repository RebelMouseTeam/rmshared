from typing import Any
from typing import TypeVar

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables import operators

from rmshared.content.taxonomy.variables.traversal import visitors
from rmshared.content.taxonomy.variables.traversal.abc import IOperators

Label = TypeVar('Label')


class Labels(core.traversal.ILabels[operators.Operator[Label]]):
    def __init__(self, operators_: IOperators[Label], delegate: core.traversal.ILabels[Label]):
        self.operators = operators_
        self.delegate = delegate

    def traverse_labels(self, labels_, visitor):
        self.operators.traverse_operators(labels_, visitor=self.LabelsVisitor(self.delegate, visitor))

    class LabelsVisitor(visitors.IOperators, visitors.IArguments, visitors.IValues, IOperators.IVisitor):
        def __init__(self, delegate: core.traversal.ILabels[Label], visitor: Any):
            self.delegate = delegate
            self.visitor = visitor

        def visit_operator(self, operator):
            return visitors.Operators(self.visitor).visit_operator(operator)

        def visit_argument(self, argument):
            return visitors.Arguments(self.visitor).visit_argument(argument)

        def visit_constant(self, constant):
            return visitors.Values(self.visitor).visit_constant(constant)

        def visit_variable(self, variable):
            return visitors.Values(self.visitor).visit_variable(variable)

        def traverse_cases(self, cases):
            self.delegate.traverse_labels(cases, self.visitor)
