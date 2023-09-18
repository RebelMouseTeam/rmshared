from rmshared.content.taxonomy.core.protocols import db
from rmshared.content.taxonomy.core.protocols import ui
from rmshared.content.taxonomy.core.protocols.abc import IBuilder
from rmshared.content.taxonomy.core.protocols.abc import IComposite
from rmshared.content.taxonomy.core.protocols.abc import IFilters
from rmshared.content.taxonomy.core.protocols.abc import ILabels
from rmshared.content.taxonomy.core.protocols.abc import IRanges
from rmshared.content.taxonomy.core.protocols.abc import IFields
from rmshared.content.taxonomy.core.protocols.abc import IValues
from rmshared.content.taxonomy.core.protocols.abc import IEvents
from rmshared.content.taxonomy.core.protocols.composite import Composite


class Factory:
    @classmethod
    def make_instance_for_ui(cls) -> 'Factory':
        return cls(builder=ui.Builder())

    @classmethod
    def make_instance_for_db(cls) -> 'Factory':
        return cls(builder=db.Builder())

    def __init__(self, builder: IBuilder):
        self.builder = builder

    def make_composite(self) -> IComposite:
        values = self.builder.make_values()
        events = self.builder.make_events()
        fields = self.builder.make_fields()
        labels = self.builder.make_labels(fields, values)
        ranges = self.builder.make_ranges(fields, values)
        filters = self.builder.make_filters(labels, ranges)
        return Composite(filters, labels, ranges, fields, events, values)

    def make_filters(self) -> IFilters:
        values = self.builder.make_values()
        fields = self.builder.make_fields()
        labels = self.builder.make_labels(fields, values)
        ranges = self.builder.make_ranges(fields, values)
        return self.builder.make_filters(labels, ranges)

    def make_labels(self) -> ILabels:
        values = self.builder.make_values()
        fields = self.builder.make_fields()
        return self.builder.make_labels(fields, values)

    def make_ranges(self) -> IRanges:
        values = self.builder.make_values()
        fields = self.builder.make_fields()
        return self.builder.make_ranges(fields, values)

    def make_fields(self) -> IFields:
        return self.builder.make_fields()

    def make_events(self) -> IEvents:
        return self.builder.make_events()

    def make_values(self) -> IValues:
        return self.builder.make_values()
