from abc import ABCMeta
from abc import abstractmethod
from operator import attrgetter
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import dict_from_list
from rmshared.tools import parse_name_and_info
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Case
from rmshared.content.taxonomy.variables.protocols.abc import IVariables

Value = TypeVar('Value', bound=values.Value)


class Values(core.protocols.IValues[values.Value]):
    def __init__(self, variables: IVariables, delegate: core.protocols.IValues):
        self.value_to_delegate_map: Mapping[Type[Value], 'Values.IDelegate[Value]'] = ensure_map_is_complete(values.Value, {
            values.Variable: self.Variable(variables),
            values.Constant: self.Constant(delegate),
        })
        self.value_name_to_delegate_map: Mapping[str, 'Values.IDelegate'] = dict_from_list(
            source=self.value_to_delegate_map.values(),
            key_func=attrgetter('name'),
        )

    def make_value(self, data):
        name, info = parse_name_and_info(data)
        return self.value_name_to_delegate_map[name].make_value(info)

    def jsonify_value(self, value):
        delegate = self.value_to_delegate_map[type(value)]
        return {delegate.name: delegate.jsonify_value_info(value)}

    class IDelegate(Generic[Value, Case], metaclass=ABCMeta):
        @property
        @abstractmethod
        def name(self) -> str:
            pass

        @abstractmethod
        def make_value(self, info: Any) -> Value:
            pass

        @abstractmethod
        def jsonify_value_info(self, value: Value) -> Any:
            pass

    class Variable(IDelegate[values.Variable, Case]):
        def __init__(self, variables: IVariables):
            self.variables = variables

        @property
        def name(self):
            return '@variable'

        def make_value(self, info: Mapping[str, Any]) -> values.Variable:
            return values.Variable(
                ref=self.variables.make_reference(info['ref']),
                index=int(info['index']),
            )

        def jsonify_value_info(self, value: values.Variable) -> Mapping[str, Any]:
            return {
                'ref': self.variables.jsonify_reference(value.ref),
                'index': value.index,
            }

    class Constant(IDelegate[values.Constant, Case]):
        def __init__(self, delegate: core.protocols.IValues):
            self.delegate = delegate

        @property
        def name(self):
            return '@constant'

        def make_value(self, info: Any) -> values.Constant:
            return values.Constant(value=self.delegate.make_value(info))

        def jsonify_value_info(self, value: values.Constant) -> Any:
            return self.delegate.jsonify_value(value.value)
