from contextlib import contextmanager
from dataclasses import replace

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.filters import Filters
from rmshared.content.taxonomy.core.traversal.labels import Labels
from rmshared.content.taxonomy.core.traversal.ranges import Ranges


class TestFilters:
    @fixture
    def traverser(self) -> Filters:
        return Filters(labels_=Labels(), ranges_=Ranges())

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_filters(self, fakes: Fakes, traverser: Filters):
        class Visitor(visitors.IFilters, visitors.ILabels, visitors.IRanges):
            def __init__(self):
                self.visits = []

            def visit_filter(self, filter_):
                self.visits.append(('visit_filter', filter_))

            def visit_label(self, label):
                self.visits.append(('visit_label', label))

            def visit_range(self, range_):
                self.visits.append(('visit_range', range_))

        visitor = Visitor()
        label_1 = fakes.make_label()
        label_2 = fakes.make_label()
        label_3 = fakes.make_label()
        range_1 = fakes.make_range()
        range_2 = fakes.make_range()
        range_3 = fakes.make_range()
        filter_1 = fakes.make_any_label_filter()
        filter_1 = replace(filter_1, labels=(label_1, label_2))
        filter_2 = fakes.make_no_labels_filter()
        filter_2 = replace(filter_2, labels=(label_3,))
        filter_3 = fakes.make_any_range_filter()
        filter_3 = replace(filter_3, ranges=(range_1,))
        filter_4 = fakes.make_no_ranges_filter()
        filter_4 = replace(filter_4, ranges=(range_2, range_3))
        traverser.traverse_filters(filters_=(filter_1, filter_2, filter_3, filter_4), visitor=visitor)

        assert visitor.visits == [
            ('visit_filter', filter_1),
            ('visit_label', label_1),
            ('visit_label', label_2),
            ('visit_filter', filter_2),
            ('visit_label', label_3),
            ('visit_filter', filter_3),
            ('visit_range', range_1),
            ('visit_filter', filter_4),
            ('visit_range', range_2),
            ('visit_range', range_3),
        ]

    def test_it_should_traverse_filters_with_context_manager(self, fakes: Fakes, traverser: Filters):
        class Visitor(visitors.IFilters, visitors.ILabels, visitors.IRanges):
            def __init__(self):
                self.visits = []

            @contextmanager
            def visit_filter(self, filter_):
                self.visits.append(('enter_filter', filter_))
                yield
                self.visits.append(('leave_filter', filter_))

            @contextmanager
            def visit_label(self, label):
                self.visits.append(('enter_label', label))
                yield
                self.visits.append(('leave_label', label))

            @contextmanager
            def visit_range(self, range_):
                self.visits.append(('enter_range', range_))
                yield
                self.visits.append(('leave_range', range_))

        visitor = Visitor()
        label_1 = fakes.make_label()
        label_2 = fakes.make_label()
        label_3 = fakes.make_label()
        range_1 = fakes.make_range()
        range_2 = fakes.make_range()
        range_3 = fakes.make_range()
        filter_1 = fakes.make_any_label_filter()
        filter_1 = replace(filter_1, labels=(label_1, label_2))
        filter_2 = fakes.make_no_labels_filter()
        filter_2 = replace(filter_2, labels=(label_3,))
        filter_3 = fakes.make_any_range_filter()
        filter_3 = replace(filter_3, ranges=(range_1,))
        filter_4 = fakes.make_no_ranges_filter()
        filter_4 = replace(filter_4, ranges=(range_2, range_3))
        traverser.traverse_filters(filters_=(filter_1, filter_2, filter_3, filter_4), visitor=visitor)

        assert visitor.visits == [
            ('enter_filter', filter_1),
            ('enter_label', label_1),
            ('leave_label', label_1),
            ('enter_label', label_2),
            ('leave_label', label_2),
            ('leave_filter', filter_1),
            ('enter_filter', filter_2),
            ('enter_label', label_3),
            ('leave_label', label_3),
            ('leave_filter', filter_2),
            ('enter_filter', filter_3),
            ('enter_range', range_1),
            ('leave_range', range_1),
            ('leave_filter', filter_3),
            ('enter_filter', filter_4),
            ('enter_range', range_2),
            ('leave_range', range_2),
            ('enter_range', range_3),
            ('leave_range', range_3),
            ('leave_filter', filter_4)
        ]
