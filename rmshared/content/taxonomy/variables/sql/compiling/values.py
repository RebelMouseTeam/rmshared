from __future__ import annotations

from collections.abc import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.sql.compiling.abc import IVariables

V = TypeVar('V', bound=values.Value)
D = TypeVar('D')


class Values(core.sql.compiling.IValues[values.Value]):
    def __init__(self, variables: IVariables, delegate: core.sql.compiling.IValues[D]):
        self.variables = variables
        self.delegate = delegate
        self.value_to_make_tree_func_map: Mapping[Type[V], compiling.MakeTreeFunc[V]] = ensure_map_is_complete(values.Value, {
            values.Constant: self._make_tree_from_constant,
            values.Variable: self._make_tree_from_variable,
        })

    def make_tree_from_value(self, value: values.Value):
        return self.value_to_make_tree_func_map[type(value)](value)

    def _make_tree_from_constant(self, constant: values.Constant) -> compiling.ITree:
        return self.delegate.make_tree_from_value(constant.value)

    def _make_tree_from_variable(self, variable: values.Variable) -> compiling.ITree:
        name = self.variables.make_tree_from_reference(variable.ref)
        if variable.index > 1:
            item = compiling.terminals.Number(variable.index)
            return compiling.operations.ItemGetter(name, item)
        else:
            return name
