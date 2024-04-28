from rmshared.content.taxonomy.core.encoders.abc import IBuilder
from rmshared.content.taxonomy.core.encoders.keys.filters import Filters
from rmshared.content.taxonomy.core.encoders.keys.labels import Labels
from rmshared.content.taxonomy.core.encoders.keys.ranges import Ranges
from rmshared.content.taxonomy.core.encoders.keys.fields import Fields
from rmshared.content.taxonomy.core.encoders.keys.values import Values
from rmshared.content.taxonomy.core.encoders.keys.events import Events


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
