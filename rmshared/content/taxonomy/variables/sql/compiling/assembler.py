from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.sql.compiling.filters import Filters
from rmshared.content.taxonomy.variables.sql.compiling.labels import Labels
from rmshared.content.taxonomy.variables.sql.compiling.ranges import Ranges
from rmshared.content.taxonomy.variables.sql.compiling.values import Values
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class Assembler(core.sql.compiling.IAssembler):
    def __init__(self, delegate: core.sql.compiling.IAssembler):
        self.delegate = delegate
        self.variables = Variables()
        self.operators = Operators(self.variables)

    def make_filters(self, labels, ranges):
        return Filters(self.operators, delegate=self.delegate.make_filters(labels, ranges))

    def make_labels(self, fields, values):
        return Labels(self.operators, delegate=self.delegate.make_labels(fields, values))

    def make_ranges(self, fields, values):
        return Ranges(self.operators, delegate=self.delegate.make_ranges(fields, values))

    def make_fields(self):
        return self.delegate.make_fields()

    def make_events(self):
        return self.delegate.make_events()

    def make_values(self):
        return Values(self.variables, delegate=self.delegate.make_values())
