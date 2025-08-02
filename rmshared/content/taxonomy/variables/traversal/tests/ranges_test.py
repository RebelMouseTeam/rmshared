from unittest.mock import Mock
from unittest.mock import call

from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables.fakes import Fakes
from rmshared.content.taxonomy.variables.traversal import IOperators
from rmshared.content.taxonomy.variables.traversal.ranges import Ranges
from rmshared.content.taxonomy.variables.traversal.operators import Operators


class TestRanges:
    @fixture
    def traverser(self, operators: Operators, delegate: core.traversal.IRanges) -> Ranges:
        return Ranges(operators_=operators, delegate=delegate)

    @fixture
    def operators(self) -> IOperators:
        return self.Operators()

    @fixture
    def delegate(self) -> Mock | core.traversal.IRanges:
        return Mock(spec=core.traversal.IRanges)

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_range_operators(self, fakes: Fakes, traverser: Ranges, delegate: core.traversal.IRanges):
        delegate.traverse_ranges = Mock()

        visitor = Mock()
        range_1 = fakes.make_range_operator()
        range_2 = fakes.make_range_operator()
        traverser.traverse_ranges(ranges_=(range_1, range_2), visitor=visitor)

        assert delegate.traverse_ranges.call_args_list == [
            call([0, range_1], visitor),
            call([1, range_2], visitor)
        ]

    class Operators(IOperators):
        def traverse_operators(self, operators_, visitor):
            for index, operator in enumerate(operators_):
                visitor.traverse_cases(cases=[index, operator])
