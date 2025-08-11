from collections.abc import Iterable

from rmshared.sql import compiling

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.abc import Operator
from rmshared.content.taxonomy.variables.sql.compiling.abc import IOperators


class Filters(core.sql.compiling.IFilters[Operator[core.filters.Filter]]):
    def __init__(self, operators_: IOperators[Operator, core.filters.Filter], delegate: core.sql.compiling.IFilters):
        self.operators = operators_
        self.delegate = delegate

    def make_tree_from_filter(self, filter_):
        return self.operators.make_tree_from_operator(filter_, make_tree_from_cases_func=self._make_tree_from_filters)

    def _make_tree_from_filters(self, filters_: Iterable[core.filters.Filter]) -> compiling.ITree:
        expressions = tuple(map(self.delegate.make_tree_from_filter, filters_))
        if len(expressions) == 1:
            return expressions[0]
        else:
            return compiling.logical.Conjunction(expressions)
