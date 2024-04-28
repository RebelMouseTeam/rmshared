from pytest import fixture

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.encoders.keys.events import Events


class TestEvents:
    @fixture
    def encoder(self) -> Events:
        return Events()

    def test_events(self, encoder: Events):
        assert encoder.encode_event(event=events.Event(name='some-event')) == 'some-event'
