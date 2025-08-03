from contextlib import contextmanager
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
        filters.visit_filter = Mock()
        visitor = Filters(delegate=filters)

        filter_ = fakes.make_filter()
        visitor.visit_filter(filter_)
        filters.visit_filter.assert_called_once_with(filter_)

    def test_it_should_delegate_filter_visit_with_context_manager(self, fakes: Fakes, filters: IFilters | Mock):
        @contextmanager
        def visit_filter(_):
            yield

        filters.visit_filter = Mock(side_effect=visit_filter)
        visitor = Filters(delegate=filters)

        filter_ = fakes.make_filter()
        visitor.visit_filter(filter_)
        filters.visit_filter.assert_called_once_with(filter_)

    def test_it_should_not_delegate_filter_visit(self, fakes: Fakes, non_visitor: Mock):
        non_visitor.visit_filter = Mock()

        visitor = Filters(delegate=non_visitor)
        visitor.visit_filter(filter_=fakes.make_filter())

        assert non_visitor.visit_filter.call_count == 0
