from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables.protocols.abc import IOperators
from rmshared.content.taxonomy.variables.protocols.filters import Filters
from rmshared.content.taxonomy.variables.protocols.labels import Labels
from rmshared.content.taxonomy.variables.protocols.ranges import Ranges


class Builder(core.protocols.IBuilder):
    def __init__(self, operators: IOperators, values: core.protocols.IValues, delegate: core.protocols.IBuilder, returns: IOperators):
        self.operators = operators
        self.values = values
        self.delegate = delegate
        self.returns = returns  # TODO: Get rid of it

    def make_filters(self, labels, ranges):
        return Filters(self.operators, delegate=self.delegate.make_filters(labels, ranges))

    def make_labels(self, fields, values):
        return Labels(self.returns, delegate=self.delegate.make_labels(fields, values))

    def make_ranges(self, fields, values):
        return Ranges(self.returns, delegate=self.delegate.make_ranges(fields, values))

    def make_fields(self):
        return self.delegate.make_fields()

    def make_events(self):
        return self.delegate.make_events()

    def make_values(self):
        return self.values
