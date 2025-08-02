from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal.visitors.abc import IValues
from rmshared.content.taxonomy.variables.traversal.visitors.values import Values


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

    def test_it_should_delegate_constant_visit(self, fakes: Fakes, values: IValues | Mock):
        values.visit_constant = Mock()
        visitor = Values(delegate=values)

        constant = fakes.make_constant()
        visitor.visit_constant(constant)

        values.visit_constant.assert_called_once_with(constant)

    def test_it_should_not_delegate_constant_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Values(delegate=non_visitor)

        constant = fakes.make_constant()
        visitor.visit_constant(constant)

        assert not hasattr(non_visitor, 'visit_constant') or not non_visitor.visit_constant.called

    def test_it_should_delegate_variable_visit(self, fakes: Fakes, values: IValues | Mock):
        values.visit_variable = Mock()
        visitor = Values(delegate=values)

        variable = fakes.make_variable()
        visitor.visit_variable(variable)

        values.visit_variable.assert_called_once_with(variable)

    def test_it_should_not_delegate_variable_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Values(delegate=non_visitor)

        variable = fakes.make_variable()
        visitor.visit_variable(variable)

        assert not hasattr(non_visitor, 'visit_variable') or not non_visitor.visit_variable.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Values(delegate=None)
        visitor.visit_constant(constant=fakes.make_constant())
        visitor.visit_variable(variable=fakes.make_variable())
