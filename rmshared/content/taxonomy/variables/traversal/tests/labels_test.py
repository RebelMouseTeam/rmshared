from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal.abc import IOperators
from rmshared.content.taxonomy.variables.traversal.labels import Labels
from rmshared.content.taxonomy.variables.traversal.operators import Operators


class TestLabels:
    @fixture
    def traverser(self, operators: Operators, delegate: core.traversal.ILabels) -> Labels:
        return Labels(operators_=operators, delegate=delegate)

    @fixture
    def operators(self) -> IOperators:
        return self.Operators()

    @fixture
    def delegate(self) -> Mock | core.traversal.ILabels:
        return Mock(spec=core.traversal.ILabels)

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_label_operators(self, fakes: Fakes, traverser: Labels, delegate: core.traversal.ILabels):
        delegate.traverse_labels = Mock()

        visitor = Mock()
        label_1 = fakes.make_label_operator()
        label_2 = fakes.make_label_operator()
        traverser.traverse_labels(labels_=(label_1, label_2), visitor=visitor)

        assert delegate.traverse_labels.call_args_list == [
            call([0, label_1], visitor),
            call([1, label_2], visitor)
        ]

    class Operators(IOperators):
        def traverse_operators(self, operators_, visitor):
            for index, operator in enumerate(operators_):
                visitor.traverse_cases(cases=[index, operator])
