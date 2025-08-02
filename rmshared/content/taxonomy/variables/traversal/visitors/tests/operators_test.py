from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal.visitors.abc import IOperators
from rmshared.content.taxonomy.variables.traversal.visitors.operators import Operators


class TestOperators:
    @fixture
    def operators(self) -> IOperators | Mock:
        return Mock(spec=IOperators)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_operator_visit(self, fakes: Fakes, operators: IOperators | Mock):
        operators.enter_operator = Mock()
        operators.leave_operator = Mock()
        visitor = Operators(delegate=operators)

        operator = fakes.make_operator()
        visitor.enter_operator(operator)
        visitor.leave_operator(operator)

        operators.enter_operator.assert_called_once_with(operator)
        operators.leave_operator.assert_called_once_with(operator)

    def test_it_should_not_delegate_operator_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Operators(delegate=non_visitor)

        operator = fakes.make_operator()
        visitor.enter_operator(operator)
        visitor.leave_operator(operator)

        assert not hasattr(non_visitor, 'enter_operator') or not non_visitor.enter_operator.called
        assert not hasattr(non_visitor, 'leave_operator') or not non_visitor.leave_operator.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Operators(delegate=None)
        visitor.enter_operator(operator=fakes.make_operator())
        visitor.leave_operator(operator=fakes.make_operator())
