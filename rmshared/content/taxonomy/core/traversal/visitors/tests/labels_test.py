from contextlib import contextmanager
from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import ILabels
from rmshared.content.taxonomy.core.traversal.visitors.labels import Labels


class TestLabels:
    @fixture
    def labels(self) -> ILabels | Mock:
        return Mock(spec=ILabels)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_label_visit(self, fakes: Fakes, labels: ILabels | Mock):
        labels.visit_label = Mock()
        visitor = Labels(delegate=labels)

        label = fakes.make_label()
        visitor.visit_label(label)
        labels.visit_label.assert_called_once_with(label)

    def test_it_should_delegate_label_visit_with_context_manager(self, fakes: Fakes, labels: ILabels | Mock):
        @contextmanager
        def visit_label(_):
            yield

        labels.visit_label = Mock(side_effect=visit_label)
        visitor = Labels(delegate=labels)

        label = fakes.make_label()
        visitor.visit_label(label)
        labels.visit_label.assert_called_once_with(label)

    def test_it_should_not_delegate_label_visit(self, fakes: Fakes, non_visitor: Mock):
        non_visitor.visit_label = Mock()

        visitor = Labels(delegate=non_visitor)
        visitor.visit_label(label=fakes.make_label())

        assert non_visitor.visit_label.call_count == 0
