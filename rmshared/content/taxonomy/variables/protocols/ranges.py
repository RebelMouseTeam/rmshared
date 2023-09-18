from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.protocols.abc import IOperators

Range = TypeVar('Range')


class Ranges(core.protocols.IRanges[operators.Operator[Range]]):
    def __init__(self, operators_: IOperators[Range], delegate: core.protocols.IRanges[Range]):
        self.operators = operators_
        self.delegate = delegate

    def jsonify_range(self, range_):
        return self.operators.jsonify_operator(range_, self.delegate.jsonify_range)

    def make_range(self, data):
        return self.operators.make_operator(data, self.delegate.make_range)
