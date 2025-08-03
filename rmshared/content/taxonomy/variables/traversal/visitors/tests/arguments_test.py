from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal.visitors.abc import IArguments
from rmshared.content.taxonomy.variables.traversal.visitors.arguments import Arguments


class TestArguments:
    @fixture
    def arguments(self) -> IArguments | Mock:
        return Mock(spec=IArguments)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_argument_visit(self, fakes: Fakes, arguments: IArguments | Mock):
        arguments.visit_argument = Mock()
        visitor = Arguments(delegate=arguments)

        argument = fakes.make_argument_type()
        visitor.visit_argument(argument)

        arguments.visit_argument.assert_called_once_with(argument)

    def test_it_should_not_delegate_argument_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Arguments(delegate=non_visitor)

        argument = fakes.make_argument_type()
        visitor.visit_argument(argument)

        assert not hasattr(non_visitor, 'visit_argument') or not non_visitor.visit_argument.called
