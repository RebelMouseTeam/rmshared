from typing import Any
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.traversal.abc import IOperators

Filter = TypeVar('Filter')


class Filters(core.traversal.IFilters[operators.Operator[Filter]]):
    def __init__(self, operators_: IOperators[Filter], delegate: core.traversal.IFilters[Filter]):
        self.operators = operators_
        self.delegate = delegate

    def traverse_filters(self, filters_, visitor):
        self.operators.traverse_operators(filters_, visitor=self.FiltersVisitor(self.delegate, visitor))

    class FiltersVisitor(IOperators.IVisitor):
        def __init__(self, delegate: core.traversal.IFilters[Filter], visitor: Any):
            self.delegate = delegate
            self.visitor = visitor

        def traverse_cases(self, cases):
            self.delegate.traverse_filters(cases, self.visitor)
