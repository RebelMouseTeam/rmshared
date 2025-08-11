from __future__ import annotations

from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.abc import IAssembler
from rmshared.content.taxonomy.core.sql.compiling.abc import IComposite
from rmshared.content.taxonomy.core.sql.compiling.assembler import Assembler
from rmshared.content.taxonomy.core.sql.compiling.composite import Composite


class Factory:
    @classmethod
    def make_instance(cls, descriptors: IDescriptors) -> Factory:
        return cls(assembler=Assembler(descriptors))

    def __init__(self, assembler: IAssembler):
        self.assembler = assembler

    def make_composite(self) -> IComposite:
        values = self.assembler.make_values()
        events = self.assembler.make_events()
        fields = self.assembler.make_fields()
        labels = self.assembler.make_labels(fields, values)
        ranges = self.assembler.make_ranges(fields, values)
        filters = self.assembler.make_filters(labels, ranges)
        return Composite(filters, labels, ranges, fields, events, values)
