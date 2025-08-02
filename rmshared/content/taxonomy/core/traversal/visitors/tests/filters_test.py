from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import IFilters
from rmshared.content.taxonomy.core.traversal.visitors.filters import Filters


class TestFilters:
    @fixture
    def filters(self) -> IFilters | Mock:
        return Mock(spec=IFilters)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_filter_visit(self, fakes: Fakes, filters: IFilters | Mock):
        filters.enter_filter = Mock()
        filters.leave_filter = Mock()
        visitor = Filters(delegate=filters)

        filter_ = fakes.make_filter()
        visitor.enter_filter(filter_)
        visitor.leave_filter(filter_)

        filters.enter_filter.assert_called_once_with(filter_)
        filters.leave_filter.assert_called_once_with(filter_)

    def test_it_should_not_delegate_filter_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Filters(delegate=non_visitor)

        filter_ = fakes.make_filter()
        visitor.enter_filter(filter_)
        visitor.leave_filter(filter_)

        assert not hasattr(non_visitor, 'enter_filter') or not non_visitor.enter_filter.called
        assert not hasattr(non_visitor, 'leave_filter') or not non_visitor.leave_filter.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Filters(delegate=None)

        visitor.enter_filter(filter_=fakes.make_filter())
        visitor.leave_filter(filter_=fakes.make_filter())
