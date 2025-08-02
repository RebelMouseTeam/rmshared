from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.ranges import Ranges


class TestRanges:
    @fixture
    def traverser(self) -> Ranges:
        return Ranges()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_ranges(self, fakes: Fakes, traverser: Ranges):
        class Visitor(visitors.IRanges, visitors.IFields, visitors.IValues):
            def __init__(self):
                self.visits = []

            def enter_range(self, range_):
                self.visits.append(('enter_range', range_))

            def leave_range(self, range_):
                self.visits.append(('leave_range', range_))

            def visit_field(self, field):
                self.visits.append(('visit_field', field))

            def visit_value(self, value):
                self.visits.append(('visit_value', value))

        visitor = Visitor()
        range_1 = fakes.make_between_range()
        range_2 = fakes.make_more_than_range()
        range_3 = fakes.make_less_than_range()
        traverser.traverse_ranges([range_1, range_2, range_3], visitor)

        assert visitor.visits == [
            ('enter_range', range_1),
            ('visit_field', range_1.field),
            ('visit_value', range_1.min_value),
            ('visit_value', range_1.max_value),
            ('leave_range', range_1),
            ('enter_range', range_2),
            ('visit_field', range_2.field),
            ('visit_value', range_2.value),
            ('leave_range', range_2),
            ('enter_range', range_3),
            ('visit_field', range_3.field),
            ('visit_value', range_3.value),
            ('leave_range', range_3)
        ]
