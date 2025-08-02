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

            def enter_event(self, event):
                self.visits.append(('enter', event))

            def leave_event(self, event):
                self.visits.append(('leave', event))

        visitor = Visitor()
        event_1 = fakes.make_event()
        event_2 = fakes.make_event()
        traverser.traverse_events([event_1, event_2], visitor)

        assert visitor.visits == [
            ('enter', event_1),
            ('leave', event_1),
            ('enter', event_2),
            ('leave', event_2)
        ]

