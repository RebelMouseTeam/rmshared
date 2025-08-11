from rmshared.sql import compiling

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.abc import IEvents


class Events(IEvents[events.Event]):
    def __init__(self, descriptors: IDescriptors):
        self.descriptors = descriptors

    def make_tree_from_event(self, event: events.Event):
        alias = self.descriptors.get_event_alias(event)
        return compiling.terminals.CName(alias)
