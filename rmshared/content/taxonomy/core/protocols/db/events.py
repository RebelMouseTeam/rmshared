from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.protocols.abc import IEvents


class Events(IEvents[events.Event]):
    def make_event(self, data):
        return events.Event(name=str(data['name']))

    def jsonify_event(self, event):
        return {'name': event.name}
