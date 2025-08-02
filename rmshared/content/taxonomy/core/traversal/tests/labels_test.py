from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal import visitors
from rmshared.content.taxonomy.core.traversal.labels import Labels


class TestLabels:
    @fixture
    def traverser(self) -> Labels:
        return Labels()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_labels(self, fakes: Fakes, traverser: Labels):
        class Visitor(visitors.ILabels, visitors.IFields, visitors.IValues):
            def __init__(self):
                self.visits = []

            def enter_label(self, label):
                self.visits.append(('enter_label', label))

            def leave_label(self, label):
                self.visits.append(('leave_label', label))

            def visit_field(self, field):
                self.visits.append(('visit_field', field))

            def visit_value(self, value):
                self.visits.append(('visit_value', value))

        visitor = Visitor()
        label_1 = fakes.make_value_label()
        label_2 = fakes.make_badge_label()
        label_3 = fakes.make_empty_label()
        traverser.traverse_labels([label_1, label_2, label_3], visitor)

        assert visitor.visits == [
            ('enter_label', label_1),
            ('visit_field', label_1.field),
            ('visit_value', label_1.value),
            ('leave_label', label_1),
            ('enter_label', label_2),
            ('visit_field', label_2.field),
            ('leave_label', label_2),
            ('enter_label', label_3),
            ('visit_field', label_3.field),
            ('leave_label', label_3)
        ]
