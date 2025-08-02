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
        class Visitor(visitors.IFilters, visitors.ILabels, visitors.IRanges, visitors.IFields, visitors.IValues):
            def __init__(self):
                self.visits = []

            def enter_filter(self, filter_):
                self.visits.append(('enter_filter', filter_))

            def leave_filter(self, filter_):
                self.visits.append(('leave_filter', filter_))

            def enter_label(self, label):
                self.visits.append(('enter_label', label))

            def leave_label(self, label):
                self.visits.append(('leave_label', label))

            def enter_range(self, range_):
                self.visits.append(('enter_range', range_))

            def leave_range(self, range_):
                self.visits.append(('leave_range', range_))

            def visit_field(self, field):
                self.visits.append(('visit_field', field))

            def visit_value(self, value):
                self.visits.append(('visit_value', value))

        visitor = Visitor()
        filter_1 = fakes.make_any_label_filter()
        filter_2 = fakes.make_no_labels_filter()
        filter_3 = fakes.make_any_range_filter()
        filter_4 = fakes.make_no_ranges_filter()
        traverser.traverse_filters([filter_1, filter_2, filter_3, filter_4], visitor)

        expected_visits = []
        
        # Process filter_1 (any label filter)
        expected_visits.append(('enter_filter', filter_1))
        for label in filter_1.labels:
            expected_visits.extend([
                ('enter_label', label),
                ('visit_field', label.field)
            ])
            if hasattr(label, 'value'):
                expected_visits.append(('visit_value', label.value))
            expected_visits.append(('leave_label', label))
        expected_visits.append(('leave_filter', filter_1))
        
        # Process filter_2 (no labels filter)
        expected_visits.append(('enter_filter', filter_2))
        for label in filter_2.labels:
            expected_visits.extend([
                ('enter_label', label),
                ('visit_field', label.field)
            ])
            if hasattr(label, 'value'):
                expected_visits.append(('visit_value', label.value))
            expected_visits.append(('leave_label', label))
        expected_visits.append(('leave_filter', filter_2))
        
        # Process filter_3 (any range filter)
        expected_visits.append(('enter_filter', filter_3))
        for range_ in filter_3.ranges:
            expected_visits.extend([
                ('enter_range', range_),
                ('visit_field', range_.field)
            ])
            if hasattr(range_, 'min_value') and hasattr(range_, 'max_value'):
                expected_visits.extend([
                    ('visit_value', range_.min_value),
                    ('visit_value', range_.max_value)
                ])
            elif hasattr(range_, 'value'):
                expected_visits.append(('visit_value', range_.value))
            expected_visits.append(('leave_range', range_))
        expected_visits.append(('leave_filter', filter_3))
        
        # Process filter_4 (no ranges filter)
        expected_visits.append(('enter_filter', filter_4))
        for range_ in filter_4.ranges:
            expected_visits.extend([
                ('enter_range', range_),
                ('visit_field', range_.field)
            ])
            if hasattr(range_, 'min_value') and hasattr(range_, 'max_value'):
                expected_visits.extend([
                    ('visit_value', range_.min_value),
                    ('visit_value', range_.max_value)
                ])
            elif hasattr(range_, 'value'):
                expected_visits.append(('visit_value', range_.value))
            expected_visits.append(('leave_range', range_))
        expected_visits.append(('leave_filter', filter_4))

        assert visitor.visits == expected_visits
