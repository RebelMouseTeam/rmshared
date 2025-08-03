from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.events import Events
from rmshared.content.taxonomy.core.traversal.visitors.abc import IEvents


class TestEvents:
    @fixture
    def traverser(self) -> Events:
        return Events()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_traverse_events(self, fakes: Fakes, traverser: Events):
        class Visitor(IEvents):
            def __init__(self):
                self.visits = []

            def visit_event(self, event):
                self.visits.append(('visit_event', event))

        visitor = Visitor()
        event_1 = fakes.make_event()
        event_2 = fakes.make_event()
        traverser.traverse_events([event_1, event_2], visitor)

        assert visitor.visits == [
            ('visit_event', event_1),
            ('visit_event', event_2)
        ]
