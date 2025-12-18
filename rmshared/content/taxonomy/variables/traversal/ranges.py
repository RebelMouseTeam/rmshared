from typing import Any
from typing import TypeVar

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables import operators

from rmshared.content.taxonomy.variables.traversal import visitors
from rmshared.content.taxonomy.variables.traversal.abc import IOperators

Range = TypeVar('Range')


class Ranges(core.traversal.IRanges[operators.Operator[Range]]):
    def __init__(self, operators_: IOperators[Range], delegate: core.traversal.IRanges[Range]):
        self.operators = operators_
        self.delegate = delegate

    def traverse_ranges(self, ranges_, visitor):
        self.operators.traverse_operators(ranges_, visitor=self.RangesVisitor(self.delegate, visitor))

    class RangesVisitor(visitors.IOperators, visitors.IArguments, visitors.IValues, IOperators.IVisitor):
        def __init__(self, delegate: core.traversal.IRanges[Range], visitor: Any):
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
            self.delegate.traverse_ranges(cases, self.visitor)
