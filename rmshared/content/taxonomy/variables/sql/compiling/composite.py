from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.sql.compiling.abc import IComposite
from rmshared.content.taxonomy.variables.sql.compiling.operators import Operators
from rmshared.content.taxonomy.variables.sql.compiling.variables import Variables


class Composite(IComposite, core.sql.compiling.IComposite):
    def __init__(self, delegate: core.sql.compiling.IComposite):
        self.delegate = delegate
        self.variables = Variables()
        self.operators = Operators(self.variables)

    def make_tree_from_operator(self, operator, make_tree_from_cases_func):
        return self.operators.make_tree_from_operator(operator, make_tree_from_cases_func)

    def make_tree_from_reference(self, reference):
        return self.variables.make_tree_from_reference(reference)

    def make_tree_from_filter(self, filter_):
        return self.delegate.make_tree_from_filter(filter_)

    def make_tree_from_labels(self, labels_, matcher):
        return self.delegate.make_tree_from_labels(labels_, matcher)

    def make_tree_from_ranges(self, ranges_, matcher):
        return self.delegate.make_tree_from_ranges(ranges_, matcher)

    def make_tree_from_event(self, event):
        return self.delegate.make_tree_from_event(event)

    def make_tree_from_field(self, field):
        return self.delegate.make_tree_from_field(field)

    def make_field_operations(self, field):
        return self.delegate.make_field_operations(field)

    def make_tree_from_value(self, value):
        return self.delegate.make_tree_from_value(value)
