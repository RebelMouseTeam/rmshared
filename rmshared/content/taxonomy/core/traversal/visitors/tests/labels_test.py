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
        labels.enter_label = Mock()
        labels.leave_label = Mock()
        visitor = Labels(delegate=labels)

        label = fakes.make_label()
        visitor.enter_label(label)
        visitor.leave_label(label)

        labels.enter_label.assert_called_once_with(label)
        labels.leave_label.assert_called_once_with(label)

    def test_it_should_not_delegate_label_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Labels(delegate=non_visitor)

        label = fakes.make_label()
        visitor.enter_label(label)
        visitor.leave_label(label)

        assert not hasattr(non_visitor, 'enter_label') or not non_visitor.enter_label.called
        assert not hasattr(non_visitor, 'leave_label') or not non_visitor.leave_label.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Labels(delegate=None)
        visitor.enter_label(label=fakes.make_label())
        visitor.leave_label(label=fakes.make_label())
