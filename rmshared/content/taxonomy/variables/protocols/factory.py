from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables.protocols import db
from rmshared.content.taxonomy.variables.protocols import ui
from rmshared.content.taxonomy.variables.protocols.abc import IBuilder
from rmshared.content.taxonomy.variables.protocols.abc import IOperators
from rmshared.content.taxonomy.variables.protocols.abc import IVariables
from rmshared.content.taxonomy.variables.protocols.builder import Builder


class Factory:
    @classmethod
    def make_instance_for_ui(cls) -> 'Factory':
        return cls(builder=ui.Builder())

    @classmethod
    def make_instance_for_db(cls) -> 'Factory':
        return cls(builder=db.Builder())

    def __init__(self, builder: IBuilder):
        self.builder = builder
        self.delegate = core.protocols.Factory(builder=self._make_builder(builder))

    @staticmethod
    def _make_builder(builder: IBuilder) -> core.protocols.IBuilder:
        delegate = core.protocols.ui.Builder()
        variables = builder.make_variables()
        operators = builder.make_operators(variables)
        values = builder.make_values(variables, delegate=delegate.make_values())
        return Builder(operators, values, delegate, returns=builder.make_returns(variables))

    def make_composite(self) -> core.protocols.IComposite:
        return self.delegate.make_composite()

    def make_filters(self) -> core.protocols.IFilters:
        return self.delegate.make_filters()

    def make_labels(self) -> core.protocols.ILabels:
        return self.delegate.make_labels()

    def make_ranges(self) -> core.protocols.IRanges:
        return self.delegate.make_ranges()

    def make_fields(self) -> core.protocols.IFields:
        return self.delegate.make_fields()

    def make_events(self) -> core.protocols.IEvents:
        return self.delegate.make_events()

    def make_values(self) -> core.protocols.IValues:
        return self.delegate.make_values()

    def make_operators(self) -> IOperators:
        variables = self.builder.make_variables()
        return self.builder.make_operators(variables)

    def make_variables(self) -> IVariables:
        return self.builder.make_variables()
