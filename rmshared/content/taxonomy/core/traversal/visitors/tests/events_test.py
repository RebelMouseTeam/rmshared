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
        events.enter_event = Mock()
        events.leave_event = Mock()
        visitor = Events(delegate=events)

        event = fakes.make_event()
        visitor.enter_event(event)
        visitor.leave_event(event)

        events.enter_event.assert_called_once_with(event)
        events.leave_event.assert_called_once_with(event)

    def test_it_should_not_delegate_event_visit(self, fakes: Fakes, non_visitor: Mock):
        visitor = Events(delegate=non_visitor)

        event = fakes.make_event()
        visitor.enter_event(event)
        visitor.leave_event(event)

        assert not hasattr(non_visitor, 'enter_event') or not non_visitor.enter_event.called
        assert not hasattr(non_visitor, 'leave_event') or not non_visitor.leave_event.called

    def test_it_should_not_fail_none_delegate(self, fakes: Fakes):
        visitor = Events(delegate=None)
        visitor.enter_event(event=fakes.make_event())
        visitor.leave_event(event=fakes.make_event())
