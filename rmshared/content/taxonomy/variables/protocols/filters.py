from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.protocols.abc import IOperators

Filter = TypeVar('Filter')


class Filters(core.protocols.IFilters[operators.Operator[Filter]]):
    def __init__(self, operators_: IOperators[Filter], delegate: core.protocols.IFilters[Filter]):
        self.operators = operators_
        self.delegate = delegate

    def jsonify_filter(self, filter_):
        return self.operators.jsonify_operator(filter_, self.delegate.jsonify_filter)

    def make_filter(self, data):
        return self.operators.make_operator(data, self.delegate.make_filter)
