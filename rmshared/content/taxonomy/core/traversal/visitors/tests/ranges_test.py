from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import IRanges
from rmshared.content.taxonomy.core.traversal.visitors.ranges import Ranges


class TestRanges:
    @fixture
    def ranges(self) -> IRanges | Mock:
        return Mock(spec=IRanges)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_range_visit(self, fakes: Fakes, ranges: IRanges | Mock):
        ranges.enter_range = Mock()
        ranges.leave_range = Mock()
        visitor = Ranges(delegate=ranges)

        range_ = fakes.make_range()
        visitor.enter_range(range_)
        visitor.leave_range(range_)

        ranges.enter_range.assert_called_once_with(range_)
        ranges.leave_range.assert_called_once_with(range_)

    def test_it_should_not_delegate_range_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Ranges(delegate=non_visitor)

        range_ = fakes.make_range()
        visitor.enter_range(range_)
        visitor.leave_range(range_)

        assert not hasattr(non_visitor, 'enter_range') or not non_visitor.enter_range.called
        assert not hasattr(non_visitor, 'leave_range') or not non_visitor.leave_range.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Ranges(delegate=None)
        visitor.enter_range(range_=fakes.make_range())
        visitor.leave_range(range_=fakes.make_range())
