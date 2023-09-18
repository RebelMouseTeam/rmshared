from rmshared.content.taxonomy.core.protocols.abc import IBuilder
from rmshared.content.taxonomy.core.protocols.ui.filters import Filters
from rmshared.content.taxonomy.core.protocols.ui.labels import Labels
from rmshared.content.taxonomy.core.protocols.ui.ranges import Ranges
from rmshared.content.taxonomy.core.protocols.ui.fields import Fields
from rmshared.content.taxonomy.core.protocols.ui.values import Values
from rmshared.content.taxonomy.core.protocols.ui.events import Events


class Builder(IBuilder):
    def make_filters(self, labels, ranges):
        return Filters(labels, ranges)

    def make_labels(self, fields, values):
        return Labels(fields, values)

    def make_ranges(self, fields, values):
        return Ranges(fields, values)

    def make_fields(self):
        return Fields()

    def make_events(self):
        return Events()

    def make_values(self):
        return Values()
