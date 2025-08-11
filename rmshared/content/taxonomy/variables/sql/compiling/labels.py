from collections.abc import Collection
from dataclasses import replace
from functools import reduce
from typing import TypeVar

from rmshared.sql import compiling

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Operator
from rmshared.content.taxonomy.variables.sql.compiling.abc import IOperators

L = TypeVar('L')


class Labels(core.sql.compiling.ILabels[Operator[L]]):
    def __init__(self, operators_: IOperators[Operator, L], delegate: core.sql.compiling.ILabels):
        self.operators = operators_
        self.delegate = delegate

    def make_tree_from_labels(self, labels_, matcher):
        def _make_tree_from_operator(operator: Operator) -> compiling.ITree:
            return self.operators.make_tree_from_operator(operator, _make_tree_from_cases_func)

        def _make_tree_from_cases_func(cases: Collection[L]) -> compiling.ITree:
            return self.delegate.make_tree_from_labels(cases, matcher)

        labels_ = reduce(self._compact_returns, labels_, tuple())
        expressions = tuple(map(_make_tree_from_operator, labels_))
        return compiling.logical.Disjunction(expressions, parenthesis='()')

    @staticmethod
    def _compact_returns(operators_: tuple[Operator, ...], next_: Operator) -> tuple[Operator, ...]:
        if not operators_:
            return (next_,)

        head, last = operators_[:-1], operators_[-1]
        if isinstance(last, operators.Return) and isinstance(next_, operators.Return):
            return *head, replace(last, cases=tuple(last.cases) + tuple(next_.cases))
        else:
            return *head, last, next_
