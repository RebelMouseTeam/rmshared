from typing import Any
from typing import TypeVar

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.traversal.abc import IOperators

Label = TypeVar('Label')


class Labels(core.traversal.ILabels[operators.Operator[Label]]):
    def __init__(self, operators_: IOperators[Label], delegate: core.traversal.ILabels[Label]):
        self.operators = operators_
        self.delegate = delegate

    def traverse_labels(self, labels_, visitor):
        self.operators.traverse_operators(labels_, visitor=self.LabelsVisitor(self.delegate, visitor))

    class LabelsVisitor(IOperators.IVisitor):
        def __init__(self, delegate: core.traversal.ILabels[Label], visitor: Any):
            self.delegate = delegate
            self.visitor = visitor

        def traverse_cases(self, cases):
            self.delegate.traverse_labels(cases, self.visitor)
