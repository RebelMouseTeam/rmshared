from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.protocols.abc import IOperators

Label = TypeVar('Label')


class Labels(core.protocols.ILabels[operators.Operator[Label]]):
    def __init__(self, operators_: IOperators[Label], delegate: core.protocols.ILabels[Label]):
        self.operators = operators_
        self.delegate = delegate

    def make_label(self, data):
        return self.operators.make_operator(data, self.delegate.make_label)

    def jsonify_label(self, label):
        return self.operators.jsonify_operator(label, self.delegate.jsonify_label)
