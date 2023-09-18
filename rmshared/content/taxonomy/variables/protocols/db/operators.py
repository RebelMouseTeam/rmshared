from abc import ABCMeta
from abc import abstractmethod
from operator import attrgetter
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import map_dict
from rmshared.tools import dict_from_list
from rmshared.tools import parse_name_and_info
from rmshared.tools import ensure_map_is_complete

from rmshared.typings import read_only

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables.abc import Case
from rmshared.content.taxonomy.variables.protocols.abc import IOperators
from rmshared.content.taxonomy.variables.protocols.abc import IVariables

Operator = TypeVar('Operator', bound=operators.Operator)


class Operators(IOperators[Case]):
    def __init__(self, variables: IVariables):
        self.operator_to_delegate_map: Mapping[Type[Operator], 'Operators.IDelegate[Operator]'] = ensure_map_is_complete(operators.Operator, {
            operators.Switch: self.Switch(self, variables),
            operators.Return: self.Return(),
        })
        self.operator_name_to_delegate_map: Mapping[str, 'Operators.IDelegate'] = dict_from_list(
            source=self.operator_to_delegate_map.values(),
            key_func=attrgetter('name'),
        )

    def make_operator(self, data: Mapping[str, Any], make_case: Callable[[Any], Case]) -> operators.Operator[Case]:
        name, info = parse_name_and_info(data)
        return self.operator_name_to_delegate_map[name].make_operator(info, make_case)

    def jsonify_operator(self, operator: operators.Operator, jsonify_case: Callable[[Case], Any]) -> Mapping[str, Any]:
        delegate = self.operator_to_delegate_map[type(operator)]
        return {delegate.name: delegate.jsonify_operator_info(operator, jsonify_case)}

    class IDelegate(Generic[Operator, Case], metaclass=ABCMeta):
        @property
        @abstractmethod
        def name(self) -> str:
            pass

        @abstractmethod
        def make_operator(self, info: Any, make_case: Callable[[Any], Case]) -> Operator:
            pass

        @abstractmethod
        def jsonify_operator_info(self, operator: Operator, jsonify_case: Callable[[Case], Any]) -> Any:
            pass

    class Switch(IDelegate[operators.Switch[Case], Case]):
        def __init__(self, operators_: 'Operators', variables: IVariables):
            self.operators = operators_
            self.variables = variables

        @property
        def name(self):
            return '@switch'

        def make_operator(self, info: Mapping[str, Any], make_case) -> operators.Switch[Case]:
            return operators.Switch[Case](
                ref=self.variables.make_reference(info['@ref']),
                cases=read_only(self._make_cases(info['@cases'], make_case)),
            )

        def jsonify_operator_info(self, operator: operators.Switch[Case], jsonify_case: Callable[[Case], Any]) -> Mapping[str, Any]:
            return {
                '@ref': self.variables.jsonify_reference(operator.ref),
                '@cases': dict(self._jsonify_cases(operator.cases, jsonify_case)),
            }

        def _make_cases(self, data: Mapping[str, Any], make_case: Callable[[Any], Case]) -> Mapping[Type[arguments.Argument], operators.Return[Case]]:
            def _make_operator(operator_data: Any) -> operators.Operator[Case]:
                return self.operators.make_operator(operator_data, make_case)

            return map_dict(data, map_key_func=self.variables.make_argument, map_value_func=_make_operator)

        def _jsonify_cases(self, cases: Mapping[Type[arguments.Argument], operators.Operator[Case]], jsonify_case: Callable[[Case], Any]) -> Mapping[str, Any]:
            def _jsonify_operator(operator_: operators.Operator[Case]) -> Any:
                return self.operators.jsonify_operator(operator_, jsonify_case)

            return map_dict(cases, map_key_func=self.variables.jsonify_argument, map_value_func=_jsonify_operator)

    class Return(IDelegate[operators.Return[Case], Case]):
        @property
        def name(self):
            return '@return'

        def make_operator(self, info: Mapping[str, Iterable[Any]], make_case: Callable[[Any], Case]) -> operators.Return[Case]:
            return operators.Return[Case](cases=tuple(map(make_case, info['@cases'])))

        def jsonify_operator_info(self, operator: operators.Return[Case], jsonify_case: Callable[[Case], Any]) -> Mapping[str, list[Any]]:
            return {'@cases': list(map(jsonify_case, operator.cases))}
