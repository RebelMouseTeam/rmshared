from rmshared.content.taxonomy.variables.protocols.abc import IBuilder
from rmshared.content.taxonomy.variables.protocols.ui.operators import Operators
from rmshared.content.taxonomy.variables.protocols.ui.variables import Variables
from rmshared.content.taxonomy.variables.protocols.ui.values import Values


class Builder(IBuilder):
    def make_operators(self, variables):
        return Operators(variables)

    def make_variables(self):
        return Variables()

    def make_values(self, variables, delegate):
        return Values(variables, delegate)
