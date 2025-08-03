from collections.abc import Callable
from collections.abc import Mapping
from contextlib import AbstractContextManager
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_context_manager
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.traversal import visitors
from rmshared.content.taxonomy.variables.traversal.abc import IOperators

Case = TypeVar('Case')
Operator = TypeVar('Operator', bound=operators.Operator)
TraverseFunc = Callable[[Operator, IOperators.IVisitor], None]


class Operators(IOperators[Case]):
    def __init__(self):
        self.operator_to_traverse_cases_func_map: Mapping[Type[operators.Operator], TraverseFunc] = ensure_map_is_complete(operators.Operator, {
            operators.Switch: self._traverse_switch_cases,
            operators.Return: self._traverse_return_cases,
        })

    def traverse_operators(self, operators_, visitor):
        for operator in operators_:
            with self._visit_operator(operator, visitor=visitors.Operators(delegate=visitor)):
                self._traverse_cases(operator, visitor)

    @staticmethod
    def _visit_operator(operator: Operator, visitor: visitors.IOperators) -> AbstractContextManager[None]:
        return ensure_context_manager(delegate=visitor.visit_operator(operator))

    def _traverse_cases(self, operator: operators.Operator[Case], visitor: IOperators.IVisitor) -> None:
        self.operator_to_traverse_cases_func_map[type(operator)](operator, visitor)

    def _traverse_switch_cases(self, operator: operators.Switch[Case], visitor: IOperators.IVisitor) -> None:
        for argument, operator in operator.cases.items():
            self._visit_argument(argument, visitor=visitors.Arguments(delegate=visitor))
            self.traverse_operators(operators_=(operator,), visitor=visitor)

    @staticmethod
    def _traverse_return_cases(operator: operators.Return[Case], visitor: IOperators.IVisitor) -> None:
        visitor.traverse_cases(operator.cases)

    @staticmethod
    def _visit_argument(argument: Type[operators.Argument], visitor: visitors.IArguments) -> None:
        visitor.visit_argument(argument)
