from __future__ import annotations

from rmshared.content.taxonomy.core.traversal.abc import IAssembler
from rmshared.content.taxonomy.core.traversal.abc import IComposite
from rmshared.content.taxonomy.core.traversal.abc import IFilters
from rmshared.content.taxonomy.core.traversal.abc import ILabels
from rmshared.content.taxonomy.core.traversal.abc import IRanges
from rmshared.content.taxonomy.core.traversal.abc import IEvents
from rmshared.content.taxonomy.core.traversal.assembler import Assembler
from rmshared.content.taxonomy.core.traversal.composite import Composite


class Factory:
    @classmethod
    def make_instance(cls) -> Factory:
        return cls(assembler=Assembler())

    def __init__(self, assembler: IAssembler):
        self.assembler = assembler

    def make_composite(self) -> IComposite:
        events = self.assembler.make_events()
        labels = self.assembler.make_labels()
        ranges = self.assembler.make_ranges()
        filters = self.assembler.make_filters(labels, ranges)
        return Composite(filters, labels, ranges, events)

    def make_filters(self) -> IFilters:
        labels = self.assembler.make_labels()
        ranges = self.assembler.make_ranges()
        return self.assembler.make_filters(labels, ranges)

    def make_labels(self) -> ILabels:
        return self.assembler.make_labels()

    def make_ranges(self) -> IRanges:
        return self.assembler.make_ranges()

    def make_events(self) -> IEvents:
        return self.assembler.make_events()
