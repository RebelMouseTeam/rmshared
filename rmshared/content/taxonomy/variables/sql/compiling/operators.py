from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Set
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.sql import compiling

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.abc import Operator
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.sql.compiling.abc import IOperators
from rmshared.content.taxonomy.variables.sql.compiling.abc import IVariables

A = TypeVar('A', bound=Argument)
O = TypeVar('O', bound=Operator)
C = TypeVar('C')


class Operators(IOperators[Operator, C]):
    def __init__(self, variables: IVariables[Reference]):
        self.variables = variables

    def make_tree_from_operator(self, operator, make_tree_from_cases_func):
        return self.Delegate(self.variables, make_tree_from_cases_func).make_tree_from_operator(operator)

    class Delegate:
        def __init__(self, variables: IVariables, make_tree_from_cases_func: compiling.MakeTreeFunc):
            self.variables = variables
            self.switches = self.Switches(delegate=self)
            self.returns = self.Returns(make_tree_from_cases_func)
            self.operator_to_make_tree_func_map: Mapping[Type[O], compiling.MakeTreeFunc[O]] = ensure_map_is_complete(Operator, {
                operators.Switch: self._make_tree_from_switch,
                operators.Return: self._make_tree_from_return,
            })

        def make_tree_from_operator(self, operator: Operator) -> compiling.ITree:
            return self.operator_to_make_tree_func_map[type(operator)](operator)

        def _make_tree_from_switch(self, operator: operators.Switch) -> compiling.ITree:
            return self.switches.make_tree_from_operator(operator)

        def _make_tree_from_return(self, operator: operators.Return) -> compiling.ITree:
            return self.returns.make_tree_from_operator(operator)

        def _make_tree_from_reference(self, ref: Reference) -> compiling.ITree:
            return self.variables.make_tree_from_reference(ref)

        class Switches:
            def __init__(self, delegate: Operators.Delegate):
                self.delegate = delegate
                self.arguments_to_make_tree_func_map: Mapping[Set[Type[A]], compiling.MakeTreeFunc[operators.Switch]] = {
                    frozenset({arguments.Any}): self._make_if_null_tree,
                    frozenset({arguments.Value}): self._make_if_not_null_tree,
                    frozenset({arguments.Value, arguments.Any}): self._make_if_not_null_otherwise_tree,
                }

            def make_tree_from_operator(self, operator: operators.Switch) -> compiling.ITree:
                argument_types = frozenset(operator.cases.keys())
                return self.arguments_to_make_tree_func_map[argument_types](operator)

            def _make_if_null_tree(self, operator: operators.Switch) -> compiling.ITree:
                return compiling.conditionals.ExpressionIfCondition(
                    condition=self._make_ref_is_null_condition(operator.ref),
                    expression=self._make_tree_from_operator(operator.cases[arguments.Any]),
                )

            def _make_if_not_null_tree(self, operator: operators.Switch) -> compiling.ITree:
                return compiling.conditionals.ExpressionIfCondition(
                    condition=self._make_ref_is_not_null_condition(operator.ref),
                    expression=self._make_tree_from_operator(operator.cases[arguments.Value]),
                )

            def _make_if_not_null_otherwise_tree(self, operator: operators.Switch) -> compiling.ITree:
                return compiling.conditionals.ExpressionIfConditionOtherwiseExpression(
                    condition=self._make_ref_is_not_null_condition(operator.ref),
                    true_expression=self._make_tree_from_operator(operator.cases[arguments.Value]),
                    else_expression=self._make_tree_from_operator(operator.cases[arguments.Any]),
                )

            def _make_ref_is_null_condition(self, ref: Reference) -> compiling.ITree:
                return compiling.operations.IsNull(operand=self.delegate._make_tree_from_reference(ref))

            def _make_ref_is_not_null_condition(self, ref: Reference) -> compiling.ITree:
                return compiling.operations.IsNotNull(operand=self.delegate._make_tree_from_reference(ref))

            def _make_tree_from_operator(self, operator: Operator) -> compiling.ITree:
                return self.delegate.make_tree_from_operator(operator)

        class Returns:
            def __init__(self, make_tree_from_cases_func: compiling.MakeTreeFunc):
                self.make_tree_from_cases_func = make_tree_from_cases_func

            def make_tree_from_operator(self, operator: operators.Return) -> compiling.ITree:
                return self.make_tree_from_cases_func(operator.cases)
