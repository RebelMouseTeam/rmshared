from pytest import fixture

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.protocols.db.events import Events


class TestEvents:
    @fixture
    def protocol(self) -> Events:
        return Events()

    def test_events(self, protocol: Events):
        assert protocol.make_event(data={'name': 'some-event', 'info': {}}) == events.Event(name='some-event')
        assert protocol.jsonify_event(event=events.Event(name='some-event')) == {'name': 'some-event'}
