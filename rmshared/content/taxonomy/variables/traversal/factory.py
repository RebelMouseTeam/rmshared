from __future__ import annotations

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables.traversal.assembler import Assembler


class Factory:
    def __init__(self):
        self.delegate = core.traversal.Factory(assembler=Assembler(delegate=core.traversal.Assembler()))

    def make_composite(self) -> core.traversal.IComposite:
        return self.delegate.make_composite()

    def make_filters(self) -> core.traversal.IFilters:
        return self.delegate.make_filters()

    def make_labels(self) -> core.traversal.ILabels:
        return self.delegate.make_labels()

    def make_ranges(self) -> core.traversal.IRanges:
        return self.delegate.make_ranges()

    def make_events(self) -> core.traversal.IEvents:
        return self.delegate.make_events()
