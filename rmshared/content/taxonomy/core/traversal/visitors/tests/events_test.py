from contextlib import contextmanager
from unittest.mock import Mock

from pytest import fixture

from rmshared.content.taxonomy.core.fakes import Fakes
from rmshared.content.taxonomy.core.traversal.visitors.abc import IEvents
from rmshared.content.taxonomy.core.traversal.visitors.events import Events


class TestEvents:
    @fixture
    def events(self) -> IEvents | Mock:
        return Mock(spec=IEvents)

    @fixture
    def non_visitor(self) -> Mock:
        return Mock()

    @fixture
    def fakes(self):
        return Fakes()

    def test_it_should_delegate_event_visit(self, fakes: Fakes, events: IEvents | Mock):
        events.visit_event = Mock()
        visitor = Events(delegate=events)

        event = fakes.make_event()
        visitor.visit_event(event)
        events.visit_event.assert_called_once_with(event)

    def test_it_should_delegate_event_visit_with_context_manager(self, fakes: Fakes, events: IEvents | Mock):
        @contextmanager
        def visit_event(_):
            yield

        events.visit_event = Mock(side_effect=visit_event)
        visitor = Events(delegate=events)

        event = fakes.make_event()
        visitor.visit_event(event)
        events.visit_event.assert_called_once_with(event)

    def test_it_should_not_delegate_event_visit(self, fakes: Fakes, non_visitor: Mock):
        non_visitor.visit_event = Mock()

        visitor = Events(delegate=non_visitor)
        visitor.visit_event(event=fakes.make_event())

        assert non_visitor.visit_event.call_count == 0
