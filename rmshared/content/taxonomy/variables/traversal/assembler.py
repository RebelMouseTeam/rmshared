from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.traversal.operators import Operators
from rmshared.content.taxonomy.variables.traversal.filters import Filters
from rmshared.content.taxonomy.variables.traversal.labels import Labels
from rmshared.content.taxonomy.variables.traversal.ranges import Ranges


class Assembler(core.traversal.IAssembler):
    def __init__(self, delegate: core.traversal.IAssembler):
        self.delegate = delegate
        self.operators = Operators()

    def make_filters(self, labels, ranges):
        return Filters(self.operators, delegate=self.delegate.make_filters(labels, ranges))

    def make_labels(self):
        return Labels(self.operators, delegate=self.delegate.make_labels())

    def make_ranges(self):
        return Ranges(self.operators, delegate=self.delegate.make_ranges())

    def make_events(self):
        return self.delegate.make_events()
