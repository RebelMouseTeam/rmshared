from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterator
from collections.abc import Mapping
from collections.abc import Set
from typing import Generic
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared import sql

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
        def __init__(self, variables: IVariables, make_tree_from_cases_func: sql.compiling.MakeTreeFunc):
            self.variables = variables
            self.operator_to_specifics_map: Mapping[Type[O], Operators.Delegate.ISpecific[O]] = ensure_map_is_complete(Operator, {
                operators.Switch: self.Switches(delegate=self),
                operators.Return: self.Returns(make_tree_from_cases_func),
            })

        def make_tree_from_operator(self, operator: Operator) -> sql.compiling.ITree:
            return self.operator_to_specifics_map[type(operator)].make_tree_from_operator(operator)

        def does_operator_have_cases(self, operator: Operator) -> bool:
            return self.operator_to_specifics_map[type(operator)].does_operator_have_cases(operator)

        def _make_tree_from_reference(self, ref: Reference) -> sql.compiling.ITree:
            return self.variables.make_tree_from_reference(ref)

        class ISpecific(Generic[O], metaclass=ABCMeta):
            @abstractmethod
            def make_tree_from_operator(self, operator: O) -> sql.compiling.ITree:
                ...

            @abstractmethod
            def does_operator_have_cases(self, operator: O) -> bool:
                ...

        class Switches(ISpecific[operators.Switch]):
            def __init__(self, delegate: Operators.Delegate):
                self.delegate = delegate
                self.arguments_to_make_tree_func_map: Mapping[Set[Type[A]], sql.compiling.MakeTreeFunc[operators.Switch]] = {
                    frozenset({arguments.Any}): self._make_if_null_tree,
                    frozenset({arguments.Value}): self._make_if_not_null_tree,
                    frozenset({arguments.Value, arguments.Any}): self._make_if_not_null_otherwise_tree,
                }

            def make_tree_from_operator(self, operator: operators.Switch) -> sql.compiling.ITree:
                argument_types = frozenset(self._stream_argument_types_with_cases(operator))
                return self.arguments_to_make_tree_func_map[argument_types](operator)

            def _stream_argument_types_with_cases(self, operator: operators.Switch) -> Iterator[Type[arguments.Argument]]:
                for argument_type, case_operator in operator.cases.items():
                    if self.delegate.does_operator_have_cases(case_operator):
                        yield argument_type

            def _make_if_null_tree(self, operator: operators.Switch) -> sql.compiling.ITree:
                return sql.compiling.conditionals.ExpressionIfCondition(
                    condition=self._make_ref_is_null_condition(operator.ref),
                    expression=self._make_tree_from_operator(operator.cases[arguments.Any]),
                )

            def _make_if_not_null_tree(self, operator: operators.Switch) -> sql.compiling.ITree:
                return sql.compiling.conditionals.ExpressionIfCondition(
                    condition=self._make_ref_is_not_null_condition(operator.ref),
                    expression=self._make_tree_from_operator(operator.cases[arguments.Value]),
                )

            def _make_if_not_null_otherwise_tree(self, operator: operators.Switch) -> sql.compiling.ITree:
                return sql.compiling.conditionals.ExpressionIfConditionOtherwiseExpression(
                    condition=self._make_ref_is_not_null_condition(operator.ref),
                    true_expression=self._make_tree_from_operator(operator.cases[arguments.Value]),
                    else_expression=self._make_tree_from_operator(operator.cases[arguments.Any]),
                )

            def _make_ref_is_null_condition(self, ref: Reference) -> sql.compiling.ITree:
                return sql.compiling.operations.IsNull(operand=self.delegate._make_tree_from_reference(ref))

            def _make_ref_is_not_null_condition(self, ref: Reference) -> sql.compiling.ITree:
                return sql.compiling.operations.IsNotNull(operand=self.delegate._make_tree_from_reference(ref))

            def _make_tree_from_operator(self, operator: Operator) -> sql.compiling.ITree:
                return self.delegate.make_tree_from_operator(operator)

            def does_operator_have_cases(self, operator: operators.Switch) -> bool:
                return any(map(self.delegate.does_operator_have_cases, operator.cases.values()))

        class Returns(ISpecific[operators.Return]):
            def __init__(self, make_tree_from_cases_func: sql.compiling.MakeTreeFunc):
                self.make_tree_from_cases_func = make_tree_from_cases_func

            def make_tree_from_operator(self, operator: operators.Return) -> sql.compiling.ITree:
                return self.make_tree_from_cases_func(operator.cases)

            def does_operator_have_cases(self, operator: operators.Return) -> bool:
                return bool(operator.cases)
