from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal.abc import IOperators
from rmshared.content.taxonomy.variables.traversal.filters import Filters
from rmshared.content.taxonomy.variables.traversal.operators import Operators


class TestFilters:
    @fixture
    def traverser(self, operators: Operators, delegate: core.traversal.IFilters) -> Filters:
        return Filters(operators_=operators, delegate=delegate)

    @fixture
    def operators(self) -> IOperators:
        return self.Operators()

    @fixture
    def delegate(self) -> Mock | core.traversal.IFilters:
        return Mock(spec=core.traversal.IFilters)

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_filter_operators(self, fakes: Fakes, traverser: Filters, delegate: core.traversal.IFilters):
        delegate.traverse_filters = Mock()

        visitor = Mock()
        filter_1 = fakes.make_filter_operator()
        filter_2 = fakes.make_filter_operator()
        traverser.traverse_filters(filters_=(filter_1, filter_2), visitor=visitor)

        assert delegate.traverse_filters.call_args_list == [
            call([0, filter_1], visitor),
            call([1, filter_2], visitor)
        ]

    class Operators(IOperators):
        def traverse_operators(self, operators_, visitor):
            for index, operator in enumerate(operators_):
                visitor.traverse_cases(cases=[index, operator])
