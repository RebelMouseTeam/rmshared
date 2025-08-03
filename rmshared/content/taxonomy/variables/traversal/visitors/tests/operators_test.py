from contextlib import contextmanager
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
        operators.visit_operator = Mock()
        visitor = Operators(delegate=operators)

        operator = fakes.make_operator()
        visitor.visit_operator(operator)
        operators.visit_operator.assert_called_once_with(operator)

    def test_it_should_delegate_operator_visit_with_context_manager(self, fakes: Fakes, operators: IOperators | Mock):
        @contextmanager
        def visit_operator(_):
            yield

        operators.visit_operator = Mock(side_effect=visit_operator)
        visitor = Operators(delegate=operators)

        operator = fakes.make_operator()
        visitor.visit_operator(operator)
        operators.visit_operator.assert_called_once_with(operator)

    def test_it_should_not_delegate_operator_visit(self, fakes: Fakes, non_visitor: Mock):
        non_visitor.visit_operator = Mock()

        visitor = Operators(delegate=non_visitor)
        visitor.visit_operator(operator=fakes.make_operator())

        assert non_visitor.visit_operator.call_count == 0
