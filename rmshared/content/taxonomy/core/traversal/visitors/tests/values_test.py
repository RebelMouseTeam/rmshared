from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import IValues
from rmshared.content.taxonomy.core.traversal.visitors.values import Values


class TestValues:
    @fixture
    def values(self) -> IValues | Mock:
        return Mock(spec=IValues)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_value_visit(self, fakes: Fakes, values: IValues | Mock):
        values.visit_value = Mock()
        visitor = Values(delegate=values)

        value = fakes.make_scalar()
        visitor.visit_value(value)

        values.visit_value.assert_called_once_with(value)

    def test_it_should_not_delegate_value_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Values(delegate=non_visitor)

        value = fakes.make_scalar()
        visitor.visit_value(value)

        assert not hasattr(non_visitor, 'visit_value') or not non_visitor.visit_value.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Values(delegate=None)
        visitor.visit_value(value=fakes.make_scalar())

    def test_it_should_not_fail_when_delegate_return_values(self, fakes: Fakes):
        class ReturningVisitor(IValues):
            def visit_value(self, value):
                return 'visited'

        visitor = Values(delegate=ReturningVisitor())
        visitor.visit_value(value=fakes.make_scalar())
