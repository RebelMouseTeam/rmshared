from contextlib import contextmanager
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
        ranges.visit_range = Mock()
        visitor = Ranges(delegate=ranges)

        range_ = fakes.make_range()
        visitor.visit_range(range_)
        ranges.visit_range.assert_called_once_with(range_)

    def test_it_should_delegate_range_visit_with_context_manager(self, fakes: Fakes, ranges: IRanges | Mock):
        @contextmanager
        def visit_range(_):
            yield

        ranges.visit_range = Mock(side_effect=visit_range)
        visitor = Ranges(delegate=ranges)

        range_ = fakes.make_range()
        visitor.visit_range(range_)
        ranges.visit_range.assert_called_once_with(range_)

    def test_it_should_not_delegate_range_visit(self, fakes: Fakes, non_visitor: Mock):
        non_visitor.visit_range = Mock()

        visitor = Ranges(delegate=non_visitor)
        visitor.visit_range(range_=fakes.make_range())

        assert non_visitor.visit_range.call_count == 0
