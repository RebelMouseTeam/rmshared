from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.protocols.abc import IEvents


class Events(IEvents[events.Event]):
    def make_event(self, data):
        name, info = parse_name_and_info(data)
        assert info == dict()
        return events.Event(name=str(name))

    def jsonify_event(self, event):
        return {event.name: dict()}
