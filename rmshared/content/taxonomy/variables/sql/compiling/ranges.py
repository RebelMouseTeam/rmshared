from collections.abc import Collection
from typing import TypeVar

from rmshared.sql import compiling

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.abc import Operator
from rmshared.content.taxonomy.variables.sql.compiling.abc import IOperators

R = TypeVar('R')


class Ranges(core.sql.compiling.IRanges[Operator[R]]):
    def __init__(self, operators_: IOperators[Operator, R], delegate: core.sql.compiling.IRanges[R]):
        self.operators = operators_
        self.delegate = delegate

    def make_tree_from_ranges(self, ranges_, matcher):
        def _make_tree_from_operator(operator: Operator) -> compiling.ITree:
            return self.operators.make_tree_from_operator(operator, _make_tree_from_cases_func)

        def _make_tree_from_cases_func(cases: Collection[R]) -> compiling.ITree:
            return self.delegate.make_tree_from_ranges(cases, matcher)

        expressions = tuple(map(_make_tree_from_operator, ranges_))
        return compiling.logical.Disjunction(expressions, parenthesis='()')
