from rmshared.content.taxonomy.core.protocols import ui
from rmshared.content.taxonomy.core.protocols.abc import IBuilder
from rmshared.content.taxonomy.core.protocols.db.fields import Fields
from rmshared.content.taxonomy.core.protocols.db.events import Events


class Builder(IBuilder):
    def __init__(self):
        self.ui = ui.Builder()  # TODO: Separate UI protocol from DB protocol

    def make_filters(self, labels, ranges):
        return self.ui.make_filters(labels, ranges)

    def make_labels(self, fields, values):
        return self.ui.make_labels(fields, values)

    def make_ranges(self, fields, values):
        return self.ui.make_ranges(fields, values)

    def make_fields(self):
        return Fields()

    def make_events(self):
        return Events()

    def make_values(self):
        return self.ui.make_values()
